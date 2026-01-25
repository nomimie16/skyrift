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

    # Proportions relatives des panneaux
    STATS_RATIO = 0.32
    SELECTION_RATIO = 0.20
    DRAGONS_RATIO = 0.48

    SPACING = 8

    def __init__(self):
        # Marges dynamiques basees sur la taille de l'ecran
        margin_top = max(70, int(sc.SCREEN_H * 0.08))
        margin_bottom = max(100, int(sc.SCREEN_H * 0.12))

        # Calcul de la largeur disponible
        grid_end_x = sc.OFFSET_X + sc.GRID_W
        available_width = sc.SCREEN_W - grid_end_x - 10

        self.panel_width = min(280, available_width - 20)
        self.panel_x = grid_end_x + (available_width - self.panel_width) // 2

        # Hauteur disponible pour les panneaux
        available_height = sc.SCREEN_H - margin_top - margin_bottom - 2 * self.SPACING

        self.stats_height = int(available_height * self.STATS_RATIO)
        self.selection_height = int(available_height * self.SELECTION_RATIO)
        self.dragons_height = int(available_height * self.DRAGONS_RATIO)

        total_height = self.stats_height + self.selection_height + self.dragons_height + 2 * self.SPACING

        start_y = margin_top + (sc.SCREEN_H - margin_top - margin_bottom - total_height) // 2

        stats_y = start_y
        selection_y = stats_y + self.stats_height + self.SPACING
        dragons_y = selection_y + self.selection_height + self.SPACING

        # Creation des panneaux
        self.stats_panel = StatsPanel(
            width=self.panel_width,
            x=self.panel_x,
            y=stats_y,
            height=self.stats_height
        )

        self.selection_panel = SelectionPanel(
            width=self.panel_width,
            x=self.panel_x,
            y=selection_y,
            height=self.selection_height
        )

        self.dragons_panel = DragonsPanel(
            width=self.panel_width,
            x=self.panel_x,
            y=dragons_y,
            height=self.dragons_height
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
