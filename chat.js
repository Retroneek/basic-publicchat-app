var client_name = prompt("Username:");
var client_id = Date.now();
document.querySelector("#ws-id").textContent = client_name;

const client_json_data = {
  "username" : client_name,
  "id" : client_id
}

fetch("/get-users", {
method: "POST",
headers: { "Content-Type": "application/json" },
body: JSON.stringify(client_json_data)});

let wsuser;

wsuser = new WebSocket(`ws://127.0.0.1:8000/ws`);

wsuser.onmessage = function (event) {
  var messages = document.getElementById("messages");
  var message = document.createElement("li");
  var content = document.createTextNode(event.data);
  message.appendChild(content);
  messages.appendChild(message);
};

function sendMessage(event) {
  var input = (document.getElementById("messageText"));
  let full_data = JSON.stringify({
    "message": input.value,
    "id:": client_id,
    "user": client_name
  });

  wsuser.send(full_data);
  input.value = "";
  event.preventDefault();
};