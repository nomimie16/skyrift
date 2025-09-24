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
        

if __name__ == "__main__":
    print("=== TEST ECONOMY ===")
    economy = Economy()
    print("golds initiaux:", economy.get_gold())  # attendu: 100
    economy.spend_gold(30)
    print("golds après dépense de 30:", economy.get_gold())  # attendu: 70
    economy.earn_gold(50)
    print("golds après gain de 50:", economy.get_gold())  # attendu: 120
    print("Peut dépenser 100:", economy.can_afford(100))  # attendu: True
    print("Peut dépenser 200:", economy.can_afford(200))  # attendu: False
    try:
        economy.spend_gold(200)
    except ValueError as e:
        print("Erreur attendue:", e)  # attendu: Not enough gold
    try:
        economy.spend_gold(100)
        print("golds après dépense de 100:", economy.get_gold())  # attendu: 20
    except ValueError as e:
        print("Erreur inattendue:", e)