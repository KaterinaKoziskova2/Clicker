import json
import time
import threading

SAVE_FILE = "game_save.json"

class ClickerGame:
    def __init__(self):
        self.points = 0
        self.buildings = {
            "Farm": {"count": 0, "base_income": 1, "upgrades": 0, "upgrade_bonus": 1},
            "Factory": {"count": 0, "base_income": 5, "upgrades": 0, "upgrade_bonus": 2},
            "Mine": {"count": 0, "base_income": 10, "upgrades": 0, "upgrade_bonus": 5},
        }
        self.load_game()
        self.running = True
        threading.Thread(target=self.passive_income, daemon=True).start()

    def save_game(self):
        with open(SAVE_FILE, "w") as f:
            json.dump({"points": self.points, "buildings": self.buildings}, f, indent=4)

    def load_game(self):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                self.points = data.get("points", 0)
                self.buildings = data.get("buildings", self.buildings)
        except FileNotFoundError:
            pass

    def click(self):
        self.points += 1
        self.save_game()
        print(f"Clicked! Points: {self.points}")

    def buy_building(self, building):
        if building in self.buildings:
            cost = (self.buildings[building]["count"] + 1) * 10
            if self.points >= cost:
                self.points -= cost
                self.buildings[building]["count"] += 1
                self.save_game()
                print(f"Bought {building}. New count: {self.buildings[building]['count']}")
            else:
                print("Not enough points!")
        else:
            print("Invalid building!")

    def upgrade_building(self, building):
        if building in self.buildings:
            cost = (self.buildings[building]["upgrades"] + 1) * 20
            if self.points >= cost:
                self.points -= cost
                self.buildings[building]["upgrades"] += 1
                self.save_game()
                print(f"Upgraded {building}. Upgrade level: {self.buildings[building]['upgrades']}")
            else:
                print("Not enough points!")
        else:
            print("Invalid building!")

    def passive_income(self):
        while self.running:
            time.sleep(1)
            for building, data in self.buildings.items():
                self.points += data["count"] * (data["base_income"] + data["upgrades"] * data["upgrade_bonus"])
            self.save_game()
            print(f"Passive income tick. Points: {self.points}")

    def run(self):
        while True:
            cmd = input("Enter command (click, buy [building], upgrade [building], exit): ").strip().split()
            if not cmd:
                continue
            if cmd[0] == "click":
                self.click()
            elif cmd[0] == "buy" and len(cmd) > 1:
                self.buy_building(cmd[1])
            elif cmd[0] == "upgrade" and len(cmd) > 1:
                self.upgrade_building(cmd[1])
            elif cmd[0] == "exit":
                self.running = False
                self.save_game()
                break
            else:
                print("Invalid command!")

if __name__ == "__main__":
    game = ClickerGame()
    game.run()