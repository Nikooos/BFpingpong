
import json
import os

DATA_FILE = "ladder.json"
LOGO_FILE = "ascii_logo.txt"
INITIAL_RATING = 1500
K_FACTOR = 32  # ELO K-factor

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"players": [], "matches": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def git_pull():
    print("\n⏬ Pulling latest changes from GitHub...")
    os.system("git pull")

def git_push(commit_msg):
    print("\n⏫ Pushing changes to GitHub...")
    os.system("git add ladder.json")
    os.system(f"git commit -m \"{commit_msg}\"")
    os.system("git push")

def print_logo():
    if os.path.exists(LOGO_FILE):
        with open(LOGO_FILE, "r") as f:
            print(f.read())

def main_menu():
    while True:
        # print_logo()
        print("\n\033[1;38;5;208m** Welcome at the Basic-Fit pingpong league 🏓 **")
        print("\nWhat do you want to do?\033[0m")
        print("1. Add Player")
        print("2. Add match")
        print("3. Watch ranking")
        print("4. Read the rules")
        print("5. Stop")

        choice = input("\n\033[4;38;5;208mSelect (1-5):\033[0m ").strip()
        if choice == "1":
            add_player()
        elif choice == "2":
            add_match()
        elif choice == "3":
            show_ladder()
        elif choice == "4":
            show_rules()
        elif choice == "5":
            break
        else:
            print("\n\033[1;31mYou're not a QA for this. Select something good!\033[0m\n\n")

def add_player():
    git_pull()
    data = load_data()
    name = input("\033[4;38;5;208mAdd name for the player (firstname lastname or STOP to cancel):\033[0m ").strip()
    if name.lower() == "stop":
        return
    if name in [p["name"] for p in data["players"]]:
        print("\033[1;31mThis player is already added!\033[0m\n\n")
        return
    data["players"].append({"name": name, "rating": INITIAL_RATING})
    save_data(data)
    git_push(f"Added player '{name}'")
    print(f"\033[1;32mPlayer '{name}' added!\033[0m\n\n")

def list_players(data):
    for i, p in enumerate(data["players"], 1):
        print(f"{i}. {p['name']} ({p['rating']})")
    return data["players"]

def get_player_selection(prompt, data):
    list_players(data)
    while True:
        sel = input(prompt + "\033[4;38;5;208m (or STOP to cancel):\033[0m ").strip()
        if sel.lower() == "stop":
            return None
        try:
            i = int(sel) - 1
            if 0 <= i < len(data["players"]):
                return data["players"][i]
        except ValueError:
            pass
        print("\033[1;31mYou're testing again? Try again.\033[0m\n\n")

def add_match():
    git_pull()
    data = load_data()
    if len(data["players"]) < 2:
        print("\033[1;31mYou can't play solo at pingpong!\033[0m\n\n")
        return

    print("\033[1;38;5;208mSelect player 1 (winner):\033[0m")
    p1 = get_player_selection("\033[4;38;5;208mNumber:\033[0m", data)
    if not p1:
        return

    print("\033[1;38;5;208mSelect player 2 (loser):\033[0m")
    while True:
        p2 = get_player_selection("\033[4;38;5;208mNumber:\033[0m", data)
        if p2 is None:
            return
        if p2["name"] != p1["name"]:
            break
        print("\033[1;31mPlayer 2 can't be the same as player 1.\033[0m\n\n")

    score = input("Enter result (eg. 11-9, 11-6, 11-8): ").strip()

    update_elo(p1, p2)
    data["matches"].append({"winner": p1["name"], "loser": p2["name"], "score": score})
    save_data(data)
    git_push(f"Match {p1['name']} vs {p2['name']}")
    print("Match added and the ranking is updated!\n")

def update_elo(winner, loser):
    expected_winner = 1 / (1 + 10 ** ((loser["rating"] - winner["rating"]) / 400))
    expected_loser = 1 / (1 + 10 ** ((winner["rating"] - loser["rating"]) / 400))
    winner["rating"] += int(K_FACTOR * (1 - expected_winner))
    loser["rating"] += int(K_FACTOR * (0 - expected_loser))

def show_ladder():
    git_pull()
    data = load_data()
    sorted_players = sorted(data["players"], key=lambda p: p["rating"], reverse=True)
    # print_logo()
    print("\n\t\033[1;38;5;208m🏓 Current ranking:\033[0m\n")
    for i, p in enumerate(sorted_players, 1):
        if i == 1:
            print(f"\033[38;5;208m\t 🏆 {p['name']:<20}{p['rating']} points\033[0m")
        elif i == 2:
            print(f"\033[38;5;250m\t 🥈 {p['name']:<20}{p['rating']} points\033[0m")
        elif i == 3:
            print(f"\033[38;5;94m\t 🥉 {p['name']:<20}{p['rating']} points\033[0m")
        else:
            print(f"\033[38;5;245m\t{i:2}. {p['name']:<20}{p['rating']} points\033[0m")
    print("\n\n")

def show_rules():
    print("\n\n\033[1;38;5;208mBasic-Fit pingpong league rules:\033[0m")
    print("- A match goes to 11 points.")
    print("- To win a match you need 2 points difference.")
    print("- Service changes every 2 points.")
    print("- At 10-10 the service changes per point.")
    print("- First service is decided by playing the ball to each other 3 times and then play for the point. Whoever wins that point gets the first serve.")
    print("- At service, the ball should first bounce on your side, then the other side. No need to be diagonally.")
    print("- You win a point if your opponent:")
    print("\t* Fails to make a correct serve or return.")
    print("\t* Lets the ball bounce twice.")
    print("\t* Hits the ball into the net or off the table.")
    print("\t* Hits the ball before letting it bounce on their side.")
    print("\nIf there is a discussion about a point, ask AI and whatever it decides is final.\n\n")

if __name__ == "__main__":
    main_menu()
