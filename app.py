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

args = parser.parse_args()


#function to load data.json
def load_data(data):
    with open("data.json", "w") as file :
        json.dump(data, file, indent=4)
        
#function to load player.json
def load_coin(player_data):
    with open("player.json", "w") as file :
        json.dump(player_data, file, indent=4)
    
def mark_done(data, deed_id,player_data):
    deeds = data["deeds"]
    deed_found = False

    players = player_data["player"]
    player_one = players[1]

    for i,deed in enumerate(deeds):
        if deed["id"] == deed_id:
            deed["status"] = "done"
            load_data(data)
            deed_found = True

        

    if deed_found == True:
        print(f"Deed (ID:{deed_id}) marked")
        player_one["coin"] +=1
        load_coin(player_data)

    else:
        print(f"Deed (ID:{deed_id}) not found")

if args.command == "mark-done":
    deed_id = args.deed_id
    mark_done(data,deed_id,player_data)