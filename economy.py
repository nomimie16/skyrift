INITIAL_GOLD = 100
GOLD_PER_TURN = 75

class Economy:

    gold: int

    def __init__(self, initial_gold=INITIAL_GOLD):
        self.gold = initial_gold

    def get_gold(self):
        return self.gold

    def earn_gold(self, amount):
        self.gold += amount

    def spend_gold(self, amount):
        if amount > self.gold:
            raise ValueError("Not enough gold")
        self.gold -= amount
        