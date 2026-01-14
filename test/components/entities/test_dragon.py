from unittest.mock import MagicMock, patch

import pytest

from src import screen_const as sc
from src.component.entities.entity import Entity
from src.component.entities.dragon import Dragonnet, DragonMoyen, DragonGeant, Dragon
from src.component.grid import Grid
from src.component.position import Position
from src.const import DRAGONNET_COST, DRAGON_MOYEN_COST, DRAGON_GEANT_COST
from src.enum.type_entities import TypeEntitiesEnum

# Classe pour tester les fonctionnalités de la classe Dragon
class TestDragon(Entity):
    def setup_method_dragon(self):
        """Initialisation précédant chaque test effectué"""
        self.grid = Grid(10, 10)
        self.position = Position(2, 2)
        self.dragonnet = Dragonnet(self.position.x, self.position.y, sprite_path="../../src/assets/sprites/dragonnet.png", player="Player 1")
        self.dragon_moyen = DragonMoyen(self.position.x, self.position.y, sprite_path="../../src/assets/sprites/dragon_moyen/dragon_moyen_bleu_droite.png", player="Player 1")
        self.dragon_geant = DragonGeant(self.position.x, self.position.y, sprite_path="../../src/assets/sprites/dragon_geant/dragon_geant_bleu_droite.png", player="Player 1")
    
    def test_dragonnet_initialization(self):
        """Test de l'initialisation du Dragonnet"""
        assert self.dragonnet.name == "Dragonnet"
        assert TypeEntitiesEnum.DRAGON in self.dragonnet.type_entity
        assert self.dragonnet.max_hp == 100
        assert self.dragonnet.attack_damage == 20
        assert self.dragonnet.attack_range == 3
        assert self.dragonnet.width == 2
        assert self.dragonnet.height == 2
        assert self.dragonnet.player == "Player 1"
    
    def test_dragonmoyen_initialization(self):
        """Test de l'initialisation du Dragon Moyen"""
        assert self.dragon_moyen.name == "Dragon Moyen"
        assert TypeEntitiesEnum.DRAGON in self.dragon_moyen.type_entity
        assert self.dragon_moyen.max_hp == 300
        assert self.dragon_moyen.attack_damage == 50
        assert self.dragon_moyen.attack_range == 4
        assert self.dragon_moyen.width == 3
        assert self.dragon_moyen.height == 3
        assert self.dragon_moyen.player == "Player 1"
    
    def test_dragongeant_initialization(self):
        """Test de l'initialisation du Dragon Géant"""
        assert self.dragon_geant.name == "Dragon Géant"
        assert TypeEntitiesEnum.DRAGON in self.dragon_geant.type_entity
        assert self.dragongeant.max_hp == 600
        assert self.dragongeant.attack_damage == 100
        assert self.dragongeant.attack_range == 5
        assert self.dragongeant.width == 4
        assert self.dragongeant.height == 4
        assert self.dragongeant.player == "Player 1"
    
    def test_dragon_player_setter(self):
        """Test du setter pour le joueur du dragon"""
        self.dragonnet.player = "Player 2"
        assert self.dragonnet.player == "Player 2"
        self.dragon_moyen.player = "Player 2"
        assert self.dragon_moyen.player == "Player 2"
        self.dragon_geant.player = "Player 2"
        assert self.dragon_geant.player == "Player 2"
    
    def test_dragon_draw(self):
        """Test de la méthode de dessin du dragon (vérifie si aucune erreur n'est levée)"""
        surface = pygame.Surface((sc.SCREEN_WIDTH, sc.SCREEN_HEIGHT))
        try:
            self.dragonnet.draw(surface)
            self.dragon_moyen.draw(surface)
            self.dragon_geant.draw(surface)
            draw_successful = True
        except Exception as e:
            draw_successful = False
        assert draw_successful == True
    
    def test_dragon_attack(self):
        """Test de la méthode d'attaque du dragon (vérifie si les dégâts sont correctement appliqués)"""
        target = MagicMock()
        target.hp = 200
        self.dragonnet.attack(target)
        assert target.hp == 180  # 200 - 20
        target.hp = 200
        self.dragon_moyen.attack(target)
        assert target.hp == 150  # 200 - 50
        target.hp = 200
        self.dragon_geant.attack(target)
        assert target.hp == 100  # 200 - 100
    
    def test_dragon_move(self):
        """Test de la méthode de déplacement du dragon (vérifie si la position est correctement mise à jour)"""
        initial_x, initial_y = self.dragonnet.position.x, self.dragonnet.position.y
        self.dragonnet.move(1, 1)
        assert self.dragonnet.position.x == initial_x + 1
        assert self.dragonnet.position.y == initial_y + 1
        initial_x, initial_y = self.dragon_moyen.position.x, self.dragon_moyen.position.y
    
        self.dragon_moyen.move(2, 2)
        assert self.dragon_moyen.position.x == initial_x + 2
        assert self.dragon_moyen.position.y == initial_y + 2
        initial_x, initial_y = self.dragon_geant.position.x, self.dragon_geant.position.y
        self.dragon_geant.move(3, 3)
        assert self.dragon_geant.position.x == initial_x + 3
        assert self.dragon_geant.position.y == initial_y + 3    
    
    def teardown_method_dragon(self):
        """Nettoyage après chaque test effectué"""
        del self.dragonnet
        del self.dragon_moyen
        del self.dragon_geant
        del self.grid
        del self.position
    
@pytest.fixture
def dragon_test_fixture():
    test_dragon = TestDragon()
    test_dragon.setup_method_dragon()
    yield test_dragon
    test_dragon.teardown_method_dragon()
