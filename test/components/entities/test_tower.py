import pygame

from src import screen_const as sc
from src.component.entities.entity import Entity
from src.component.grid import Grid
from src.enum.type_entities import TypeEntitiesEnum
from src.player import Player
from src.component.entities.tower import Tower


# Classe pour tester les fonctionnalités de la classe Tower
class TestTower(Entity):
    
    def setup_method_tower(self):
        """Initialisation précédant chaque test effectué"""
        self.player = Player("Player 1", "blue")
        self.tower = Tower(5, 5, sprite_path="path/to/sprite.png", player=self.player)
    
    def test_tower_initialization(self):
        """Test de l'initialisation de la tour"""
        assert self.tower._name == "Tour de défense"
        assert TypeEntitiesEnum.TOWER in self.tower.type_entity
        assert TypeEntitiesEnum.OBSTACLE in self.tower.type_entity
        assert self.tower._max_hp == 300
        assert self.tower._attack_damage == 30
        assert self.tower._attack_range == 5
        assert self.tower._width == 2
        assert self.tower._height == 1
        assert self.tower._player == self.player
        assert self.tower._active == False
        assert self.tower._cost == 600
    
    def test_tower_activation(self):
        """Test de l'activation de la tour"""
        grid = Grid(10, 10)
        self.tower.tower_activation(grid)
        assert self.tower._active == True
        assert self.tower._height == 3
    
    def test_tower_disable(self):
        """Test de la désactivation de la tour"""
        grid = Grid(10, 10)
        self.tower.tower_activation(grid)  # Activer la tour d'abord
        self.tower.tower_disable(grid)
        assert self.tower._active == False
        assert self.tower._height == 1
    
    def test_tower_take_damage(self):
        """Test de la prise de dégâts par la tour"""
        initial_hp = self.tower._hp
        damage_amount = 50
        self.tower.take_damage(damage_amount)
        assert self.tower._hp == initial_hp - damage_amount
    def test_tower_take_damage_to_zero(self):
        """Test de la prise de dégâts qui réduit les PV de la tour à zéro"""
        self.tower.take_damage(self.tower._hp + 50)  # Infliger plus de dégâts que les PV actuels
        assert self.tower._hp == 0
    def test_tower_player_setter(self):
        """Test du setter pour le joueur de la tour"""
        new_player = Player("Player 2", "red")
        self.tower._player = new_player
        assert self.tower._player == new_player
    def test_tower_draw(self):  
        """Test de la méthode de dessin de la tour (vérifie si aucune erreur n'est levée)"""
        surface = pygame.Surface((sc.SCREEN_WIDTH, sc.SCREEN_HEIGHT))
        try:
            self.tower.draw(surface)
            draw_successful = True
        except Exception as e:
            draw_successful = False
        assert draw_successful == True
    def test_tower_cost_setter(self):
        """Test du setter pour le coût de la tour"""
        initial_cost = self.tower._cost
        self.tower._cost = 750
        assert self.tower._cost == 750
        assert self.tower._cost != initial_cost
    def test_tower_attack_damage_setter(self):
        """Test du setter pour les dégâts d'attaque de la tour"""
        initial_attack_damage = self.tower._attack_damage
        self.tower._attack_damage = 40
        assert self.tower._attack_damage == 40
        assert self.tower._attack_damage != initial_attack_damage
    def test_tower_attack_range_setter(self):
        """Test du setter pour la portée d'attaque de la tour"""
        initial_attack_range = self.tower._attack_range
        self.tower._attack_range = 7
        assert self.tower._attack_range == 7
        assert self.tower._attack_range != initial_attack_range