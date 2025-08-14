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

# Mark as done parser
mark_done_parser = subparser.add_parser("mark-done", help="mark as done parser")
mark_done_parser.add_argument("deed_id", help="add your deeds id", type=int)
mark_done_parser.add_argument("-p", "--player_id", help="your player id", type=int, required=True)

args = parser.parse_args()


#function to save data.json
def save_data(data):
    with open("data.json", "w") as file :
        json.dump(data, file, indent=4)
        
#function to save player.json
def save_coin(player_data):
    with open("player.json", "w") as file :
        json.dump(player_data, file, indent=4)
    
def mark_done(data, deed_id,player_data, player_id):
    deeds = data["deeds"]
    deed_found = False

    players = player_data["player"]
    player_found = False

    for i,deed in enumerate(deeds):
        if deed["id"] == deed_id:
            deed["status"] = "done"
            save_data(data)
            deed_found = True

        

    if deed_found == True:
        print(f"Deed (ID:{deed_id}) marked")
        for i,player in enumerate(players):
            if player["id"] == player_id:
                player["coin"] +=1
                save_coin(player_data)
                player_found = True
    else:
        print(f"Deed (ID:{deed_id}) not found")
    
    if player_found == True:
        print(f"Player (ID:{player_id}) gained 1 coin!")
    else:
        print(f"Player (ID:{player_id}) not found")


if args.command == "mark-done":
    deed_id = args.deed_id
    player_id = args.player_id
    mark_done(data,deed_id,player_data,player_id)