import argparse
import json
import os

# Create JSON file if it doesn't exist
if not os.path.exists("data.json"):
    with open("data.json", "w") as file:
        json.dump([], file)

# Open the file
with open("data.json", "r") as file :
    data = json.load(file)

# Create JSON file if it doesn't exist
if not os.path.exists("player.json"):
    with open("player.json", "w") as file:
        json.dump([], file)

# Open the file
with open("player.json", "r") as file :
    player_data = json.load(file)

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest="command", help="command for subparse")

# Login
login_parser = subparser.add_parser("login", help="login with name and password")
login_parser.add_argument("username", help="your username")
login_parser.add_argument("password", help="your password")


# Mark as done parser
mark_done_parser = subparser.add_parser("mark-done", help="mark as done parser")
mark_done_parser.add_argument("deed_id", help="add your deeds id", type=int)
mark_done_parser.add_argument("-p", "--player_id", help="your player id", type=int, required=True)

# List parser
list_parser = subparser.add_parser("list",help="list the deeds")

# Display coin parser
display_coin_parser = subparser.add_parser("coin",help="display your current coin")
display_coin_parser.add_argument("player_id", help="your player id", type=int)

# Sedekah parser
sedekah_parser = subparser.add_parser("sedekah", help="sedekah your coin!")
sedekah_parser.add_argument("player_id", help="your player id", type=int)
sedekah_parser.add_argument("-to", "--to_receiver", dest="receiver_id", help=" the id of receiver", type=int, required=True)

args = parser.parse_args()

def login(username, password, player_data):

    players = player_data["player"]
    login_success = False

    for i,player in enumerate(players):
        if player["name"] == username and player["password"] == password:
            login_success = True
            player_id = player["id"]
            break

    if login_success == True:
        print(f"Welcome {username}. You have login successfully")
        return player["id"]
    else:
        print("Your username or password are wrong")

#function to save data.json
def save_data(data):
    with open("data.json", "w") as file :
        json.dump(data, file, indent=4)

#function to save player.json
def save_coin(player_data):
    with open("player.json", "w") as file :
        json.dump(player_data, file, indent=4)

def add_coin(player_data, player_id):

    players = player_data["player"]
    player_found = False

    for i,player in enumerate(players):
        if player["id"] == player_id:
            player["coin"] +=1
            save_coin(player_data)
            player_found = True

    if player_found == True:
        print(f"Player [ID:{player_id}] gained 1 coin!")
    else:
        print(f"Player [ID:{player_id}] not found")

def mark_done(data, deed_id,player_data, player_id):

    deeds = data["deeds"]
    deed_found = False

    for i,deed in enumerate(deeds):
        if deed["id"] == deed_id:
            deed["status"] = "done"
            save_data(data)
            deed_found = True

    if deed_found == True:
        print(f"Deed [ID:{deed_id}] marked")
        add_coin(player_data, player_id)
    else:
        print(f"Deed [ID:{deed_id}] not found")

def list_deeds (data):

    deeds = data["deeds"]

    print("ID | Deeds                | Status       |")
    print("-" * 43)
    for deed in deeds:
        print(f"{deed['id']:2} | {deed['task'][:20]:<20} | {deed['status']:<12} |") #:2 means two spaces

def display_coin(player_data, player_id):

    players = player_data["player"]
    player_found = False

    for i,player in enumerate(players):
        if player["id"] == player_id:
            print(f"{player['name']} [{player['coin']}] coins")
            player_found = True

    if player_found == False:
        print(f"Player [ID:{player_id}] not found")

def sedekah(player_data, player_id, receiver_id):

    players = player_data["player"]
    player_found = False
    receiver_found = True

    for i,player in enumerate(players):
        if player["id"] == player_id:
            player_found = True
            if player["coin"] <= 0:
                print(f"Player {player['id']} have insufficient balance!")
                break
            else:
                for i,receiver in enumerate(players):
                    if receiver["id"] == receiver_id:   
                        receiver_found = True     
                        player["coin"] -=1
                        receiver["coin"] +=1
                        save_coin(player_data)
                        print(f"Player {player['id']} have sedekah 1 coin! to Player {receiver['id']}")
                    else:
                        receiver_found = False
                    

    if player_found == False:
        print(f"Player [ID:{player_id}] not found")
    if receiver_found == False:
        print(f"Receiver Player [ID:{receiver_id}] not found")        

if args.command == "login":
    username = args.username
    password = args.password
    player_id = login(username, password, player_data)
    print(player_id)
if args.command == "mark-done":
    deed_id = args.deed_id
    player_id = args.player_id
    mark_done(data,deed_id,player_data,player_id)
if args.command == "list":
    list_deeds(data)
if args.command == "coin":
    player_id = args.player_id
    display_coin(player_data, player_id)
if args.command == "sedekah":
    player_id = args.player_id
    receiver_id = args.receiver_id
    sedekah(player_data, player_id, receiver_id)