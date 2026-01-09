from enum import Enum


class TypeEventEnum(str, Enum):
    """Énumération des types d'événements du jeu"""

    MORT_ADVERSAIRE = "Un dragon adverse est mort !"
    MORT_ALLIE = "Un de vos dragons est mort !"
    TOUR_DETRUITE = "La tour adverse a été détruite"
    BASE_DETRUITE = "La base adverse a été détruite"
    NOUVEAU_DRAGON = "Un nouveau dragon a été acheté"
    NOUVELLE_TOUR = "La tour a été construite"
