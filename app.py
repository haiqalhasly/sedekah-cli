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



parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest="command", help="command for subparse")

# Mark as done parser
mark_done_parser = subparser.add_parser("mark-done", help="mark as done parser")
mark_done_parser.add_argument("deed_id", help="add your deeds id", type=int)

args = parser.parse_args()


#function to load data
def load_data(data):
    with open("data.json", "w") as file :
        json.dump(data, file, indent=4)
        

def mark_done(data, deed_id):
    deeds = data["deeds"]
    deed_found = False

    for i,deed in enumerate(deeds):
        if deed["id"] == deed_id:
            deed["status"] = "done"
            load_data(data)
            deed_found = True
        

    if deed_found == True:
        print(f"Deed (ID:{deed_id}) marked")
    else:
        print(f"Deed (ID:{deed_id}) not found")

if args.command == "mark-done":
    deed_id = args.deed_id
    mark_done(data,deed_id)