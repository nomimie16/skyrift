"""
Gere le positionnement des panneaux droits
"""
from src import screen_const as sc
from src.page.component.stats_panel import StatsPanel
from src.page.component.selection_panel import SelectionPanel
from src.page.component.dragons_panel import DragonsPanel


class PanelsLayout:
    """
    Gere le positionnement des 3 panneaux (StatPanel, SelectionPanel, DragonPanel)
    """

    # Dimensions
    STATS_HEIGHT = 230
    SELECTION_HEIGHT = 150
    DRAGONS_HEIGHT = 350

    SPACING = 8

    def __init__(self):
        # Calcul de la largeur disponible
        grid_end_x = sc.OFFSET_X + sc.GRID_W
        available_width = sc.SCREEN_W - grid_end_x - 10

        self.panel_width = min(280, available_width - 20)

        self.panel_x = grid_end_x + (available_width - self.panel_width) // 2

        total_height = self.STATS_HEIGHT + self.SELECTION_HEIGHT + self.DRAGONS_HEIGHT + 2 * self.SPACING

        available_height = sc.GRID_H
        if total_height > available_height:
            # Reduire proportionnellement les hauteurs
            scale = available_height / total_height
            self.STATS_HEIGHT = int(self.STATS_HEIGHT * scale)
            self.SELECTION_HEIGHT = int(self.SELECTION_HEIGHT * scale)
            self.DRAGONS_HEIGHT = int(self.DRAGONS_HEIGHT * scale)
            total_height = self.STATS_HEIGHT + self.SELECTION_HEIGHT + self.DRAGONS_HEIGHT + 2 * self.SPACING

        start_y = sc.OFFSET_Y + (sc.GRID_H - total_height) // 4

        stats_y = start_y
        selection_y = stats_y + self.STATS_HEIGHT + self.SPACING
        dragons_y = selection_y + self.SELECTION_HEIGHT + self.SPACING

        # Creation des panneaux
        self.stats_panel = StatsPanel(
            width=self.panel_width,
            x=self.panel_x,
            y=stats_y,
            height=self.STATS_HEIGHT
        )

        self.selection_panel = SelectionPanel(
            width=self.panel_width,
            x=self.panel_x,
            y=selection_y,
            height=self.SELECTION_HEIGHT
        )

        self.dragons_panel = DragonsPanel(
            width=self.panel_width,
            x=self.panel_x,
            y=dragons_y,
            height=self.DRAGONS_HEIGHT
        )

    def draw(self, surface, turn, p1, p2, builder, current_player, selected_dragon=None):
        """Dessine les 3 panneaux"""
        self.stats_panel.draw(surface, turn, p1, p2, builder)
        self.selection_panel.draw(surface, selected_dragon)
        self.dragons_panel.draw(surface, current_player, selected_dragon)

    def handle_click(self, pos):
        """
        Gere le clic sur les panneaux.
        """
        return self.dragons_panel.handle_click(pos)
