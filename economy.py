INITIAL_GOLD = 100 
GOLD_PER_TURN = 75 # managed in the main game loop


class Economy:

    _gold: int

    def __init__(self, initial_gold=INITIAL_GOLD):
        self._gold = initial_gold

    def get_gold(self):
        """return the current amount of gold"""
        return self._gold
    
    def set_gold(self, amount):
        """set the current amount of gold"""
        self._gold = amount

    def earn_gold(self, amount):
        """add gold to the balance"""
        self._gold += amount

    def spend_gold(self, amount):
        """try to spend gold, raise an error if there is not enough gold"""
        if amount > self._gold:
            raise ValueError("Not enough gold")
        self._gold -= amount

    def can_afford(self, amount):
        """return True if the player can afford the amount, False otherwise"""
        return self._gold >= amount
        