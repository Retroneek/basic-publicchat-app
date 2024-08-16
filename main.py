from sanic import Sanic, response, Websocket
from sanic_cors import CORS
import json

app = Sanic('chatapp')
CORS(app)

async def log_msg(incoming_log):
    stored_msg = json.load(open('log.json'))
    stored_msg["messages"].append(incoming_log)
    with open('log.json', 'w') as file:
            json.dump(stored_msg, file, indent=4)

def user_initialization(data):
    username_rejected = 0
    stored_users = json.load(open('user.json'))
    for client in stored_users["users"]:
        if data["username"] == client["username"]:
            username_rejected = 1
            break
        
    if (username_rejected == 0):
        stored_users["users"].append(data)
        print(stored_users)
        with open('user.json', 'w') as file:
            json.dump(stored_users, file, indent=4)

@app.post("/get-users")
async def get_users(request):
    try:
        user_data = request.json
        user_initialization(user_data)
        return response.text("Data received & User is stored")

    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return response.text("An error occurred", status=500)
        
@app.route("/")
async def chat(request):
    return await response.file('index.html')

app.static("/", "./")

class UserConnectionManagement:
    def __init__(self):
        self.active_connections = []
        
    async def connect(self, websocket):
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: Websocket):
        self.active_connections.remove(websocket)
        
    async def broadcast(self, message):
        for connection in self.active_connections:
            await connection.send(message)
            
user = UserConnectionManagement()

@app.websocket('/ws')
async def ws_handler(request, ws: Websocket):
    await user.connect(ws)
    try:
        while True:
            data = await ws.recv()
            full_data = json.loads(data)
            await log_msg(full_data)
            message = full_data.get("message")
            user_name = full_data.get("user")
            await user.broadcast(f"{user_name}: {message}")
    except:
        user.disconnect(ws)

if __name__ == "__main__":
    app.run(dev=True)