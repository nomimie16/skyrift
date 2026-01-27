INITIAL_GOLD: int = 100  # TODO : remttre ca a 100
GOLD_PER_TURN: int = 75  # managed in the main game loop


class Economy:
    _gold: int

    def __init__(self, initial_gold: int = INITIAL_GOLD):
        self._gold = initial_gold
        self._listeners = []

    def get_gold(self) -> int:
        """return the current amount of gold"""
        return self._gold

    def add_listener(self, callback) -> None:
        """Ajoute une fonction à appeler à chaque changement de gold
        :param callback: fonction à appeler avec le delta en paramètre
        """
        self._listeners.append(callback)

    def _notify(self, delta):
        """Notifie tous les listeners du changement"""
        for cb in self._listeners:
            cb(delta)

    def set_gold(self, amount: int):
        """set the current amount of gold"""
        self._gold = amount

    def earn_gold(self, amount: int):
        """add gold to the balance"""
        self._gold += amount
        self._notify(+amount)

    def spend_gold(self, amount: int):
        """try to spend gold, raise an error if there is not enough gold"""
        if amount > self._gold:
            raise ValueError("Not enough gold")
        self._gold -= amount
        self._notify(-amount)

    def can_afford(self, amount: int):
        """return True if the player can afford the amount, False otherwise"""
        return self._gold >= amount

    def start_turn(self):
        """Ajoute l'or gagné au début du tour"""
        self.earn_gold(GOLD_PER_TURN)
