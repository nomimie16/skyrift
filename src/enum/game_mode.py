from enum import Enum

class GameMode(Enum):
    """Modes de jeu possibles"""
    PLAYER_VS_PLAYER = "pvp"
    PLAYER_VS_AI = "pvai"
    AI_VS_AI = "aivai"