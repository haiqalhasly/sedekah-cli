import json

def reset_status(filename="player.json"):
    with open(filename) as f:
        data = json.load(f)

    for player in data["player"]:
        for deed in player["deeds"]:
            if deed["status"] == "done":
                deed["status"] = "not done"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    reset_status()
    print("✅ Reset done")
