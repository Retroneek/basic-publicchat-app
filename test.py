import json

def user_initialization(user_match: str):
    username_rejected = 0
    stored_users = json.load(open('user.json'))
    for client in stored_users["users"]:
        if user_match == client["username"]:
            print("Username is already taken")
            username_rejected = 1
            break
    if (username_rejected == 0):
        stored_users["users"].append({"username":user_match, "id":"invalid_data"})
        print("This username can be added")
        print(stored_users)
        with open('user.json', 'w') as file:
            json.dump(stored_users, file, indent=4)
            print("User Data Updated")
        
        
        
user_initialization("Evan S")