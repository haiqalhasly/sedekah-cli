import argparse
import json
import os

def is_authenticated():
    return os.path.exists("session.json")

def create_session(player_data):


    player_session_data = {
            "id": player_data["id"],
            "name": player_data["name"]
        }
    # Create JSON file if it doesn't exist
    if not os.path.exists("session.json"):
        with open("session.json", "w") as session_file:
            json.dump(player_session_data, session_file, indent=1 )
            print("Creating session...")

def clear_session():
    if os.path.exists("session.json"):
        os.remove("session.json")
        
def login(username, password, player_data):

    players = player_data["player"]
    login_success = False

    for i,player in enumerate(players):
        if player["name"] == username and player["password"] == password:
            login_success = True
            player_id = player["id"]
            create_session(player)
            break

    if login_success == True:
        print(f"Welcome {username}. You have login successfully")
        return player["id"]
    else:
        print("Your username or password are wrong")

def logout():
    clear_session()
    print("Logged out successfully")

def save_coin(player_data):
    with open("player.json", "w") as file :
        json.dump(player_data, file, indent=4)

def get_player_id (session_data):

    player_id = session_data["id"]
    return player_id


def mark_done(deed_id,player_data, player_id):

    #Find the player id

    players = player_data["player"]
    player_found = False

    for i,player in enumerate(players):
        if player["id"] == player_id:
            player["coin"] +=1
            save_coin(player_data)

        #Find the deed id

            deeds = player["deeds"]
            deed_found = False

            for i,deed in enumerate(deeds):
                if deed["id"] == deed_id:
                    deed["status"] = "done"
                    save_coin(player_data)
                    print("checking your deed...")
                    deed_found = True

            if deed_found == True:
                print(f"Deed [ID:{deed_id}] marked")
                print(f"Player [ID:{player_id}] gained 1 coin!")
            else:
                print(f"Deed [ID:{deed_id}] not found")

def list_deeds (player_data, player_id):
            
    #Find the player id

    players = player_data["player"]
    player_found = False

    for i,player in enumerate(players):
        if player["id"] == player_id:
            player["coin"] +=1
            save_coin(player_data)

        #Find the deed id

            deeds = player["deeds"]

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
                if receiver_id == player_id:
                    print("You cannot give it to yourself")
                    break
                for i,receiver in enumerate(players):
                    if receiver["id"] == receiver_id:   
                        receiver_found = True     
                        player["coin"] -=1
                        receiver["coin"] +=1
                        save_coin(player_data)
                        print(f"Player {player['id']} have sedekah 1 coin! to Player {receiver['id']}")
                        break
                    else:
                        receiver_found = False
                    

    if player_found == False:
        print(f"Player [ID:{player_id}] not found")
    if receiver_found == False:
        print(f"Receiver Player [ID:{receiver_id}] not found")        

def main():


    # Create JSON file if it doesn't exist
    if not os.path.exists("player.json"):
        with open("player.json", "w") as file:
            json.dump([], file)

    # Open the file
    with open("player.json", "r") as file :
        player_data = json.load(file)

    # Open the file
    if os.path.exists("session.json"):
        with open("session.json", "r") as session_file :
            session_data = json.load(session_file)



    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command", help="command for subparse")

    # Login
    login_parser = subparser.add_parser("login", help="login with name and password")
    login_parser.add_argument("username", help="your username")
    login_parser.add_argument("password", help="your password")

    # Logout
    logout_parser = subparser.add_parser("logout", help="logout your account")

    # Mark as done parser
    mark_done_parser = subparser.add_parser("mark-done", help="mark as done parser")
    mark_done_parser.add_argument("deed_id", help="add your deeds id", type=int)

    # List parser
    list_parser = subparser.add_parser("list",help="list the deeds")

    # Display coin parser
    display_coin_parser = subparser.add_parser("coin",help="display your current coin")

    # Sedekah parser
    sedekah_parser = subparser.add_parser("sedekah", help="sedekah your coin!")
    sedekah_parser.add_argument("-to", "--to_receiver", dest="receiver_id", help=" the id of receiver", type=int, required=True)

    args = parser.parse_args()

    if args.command == "login":
        login(args.username, args.password, player_data)
    elif args.command == "logout":
        logout()
    else: 
        if not is_authenticated():
            print("You must login first!")
            return      
        
        if args.command == "mark-done":
            deed_id = args.deed_id 
            player_id = get_player_id(session_data)
            mark_done(deed_id,player_data,player_id)
        if args.command == "list":
            player_id = get_player_id(session_data)
            list_deeds(player_data,player_id)
        if args.command == "coin":
            player_id = get_player_id(session_data)
            display_coin(player_data, player_id)
        if args.command == "sedekah":
            player_id = get_player_id(session_data)
            receiver_id = args.receiver_id
            sedekah(player_data, player_id, receiver_id)

if __name__ == "__main__":
    main()