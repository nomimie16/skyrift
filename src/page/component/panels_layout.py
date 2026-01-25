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

    # Dimensions de base (seront ajustees si necessaire)
    BASE_STATS_HEIGHT = 230
    BASE_SELECTION_HEIGHT = 150
    BASE_DRAGONS_HEIGHT = 350

    SPACING = 8
    MARGIN_TOP = 20
    MARGIN_BOTTOM = 20

    def __init__(self):
        # Calcul de la largeur disponible
        grid_end_x = sc.OFFSET_X + sc.GRID_W
        available_width = sc.SCREEN_W - grid_end_x - 10

        self.panel_width = min(280, available_width - 20)

        self.panel_x = grid_end_x + (available_width - self.panel_width) // 2

        available_height = sc.SCREEN_H - self.MARGIN_TOP - self.MARGIN_BOTTOM

        total_base_height = (self.BASE_STATS_HEIGHT + self.BASE_SELECTION_HEIGHT +
                             self.BASE_DRAGONS_HEIGHT + 2 * self.SPACING)

        if total_base_height > available_height:
            scale = available_height / total_base_height
        else:
            scale = 1.0

        self.stats_height = int(self.BASE_STATS_HEIGHT * scale)
        self.selection_height = int(self.BASE_SELECTION_HEIGHT * scale)
        self.dragons_height = int(self.BASE_DRAGONS_HEIGHT * scale)

        total_height = self.stats_height + self.selection_height + self.dragons_height + 2 * self.SPACING

        # Position Y centree verticalement avec un leger decalage vers le haut
        ideal_start_y = sc.OFFSET_Y + (sc.GRID_H - total_height) // 4

        min_start_y = self.MARGIN_TOP
        start_y = max(ideal_start_y, min_start_y)

        max_end_y = sc.SCREEN_H - self.MARGIN_BOTTOM
        if start_y + total_height > max_end_y:
            start_y = max_end_y - total_height
            if start_y < min_start_y:
                start_y = min_start_y
                # Recalculer les hauteurs pour tenir dans l'espace
                available_for_panels = max_end_y - min_start_y - 2 * self.SPACING
                scale = available_for_panels / (self.stats_height + self.selection_height + self.dragons_height)
                self.stats_height = int(self.stats_height * scale)
                self.selection_height = int(self.selection_height * scale)
                self.dragons_height = int(self.dragons_height * scale)

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
