import arcade
import arcade.gui
from level_select import LevelSelectView
from menu import MenuView

class WinView(arcade.View):
    def __init__(self, level_id, crystals):
        super().__init__()
        self.level_id = level_id
        self.crystals = crystals
        self.ui = arcade.gui.UIManager()
        self.ui.enable()

        self.setup_ui()

    def setup_ui(self):
        box = arcade.gui.UIBoxLayout(space_between=20)

        # Title
        title = arcade.gui.UILabel(
            text="LEVEL COMPLETED!",
            font_size=30,
            text_color=arcade.color.GOLD,
            font_name=("Arial",)
        )
        box.add(title)

        # Stats
        stats = arcade.gui.UILabel(
            text=f"Crystals Collected: {self.crystals}",
            font_size=20,
            text_color=arcade.color.WHITE
        )
        box.add(stats)

        # Buttons
        next_level_btn = arcade.gui.UIFlatButton(text="Next Level", width=200)
        # For now, just go to level select, or logic for next level could be added
        next_level_btn.on_click = lambda e: self.window.show_view(LevelSelectView())
        box.add(next_level_btn)

        menu_btn = arcade.gui.UIFlatButton(text="Main Menu", width=200)
        menu_btn.on_click = lambda e: self.window.show_view(MenuView())
        box.add(menu_btn)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(box, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(anchor)

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)
        self.ui.draw()

    def on_hide_view(self):
        self.ui.disable()
