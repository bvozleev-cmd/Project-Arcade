import arcade
import arcade.gui
from game import MyGame
from database import get_levels
from menu import MenuView


class LevelSelectView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui = arcade.gui.UIManager()
        self.ui.enable()

        box = arcade.gui.UIBoxLayout(space_between=15)

        for level_id, completed, crystals in get_levels():
            status = "✔" if completed else "✖"
            text = f"Level {level_id} [{status}] 💎 {crystals}/10"
            btn = arcade.gui.UIFlatButton(text=text, width=420)
            btn.on_click = lambda e, lvl=level_id: self.start(lvl)
            box.add(btn)

        back = arcade.gui.UIFlatButton(text="Back", width=200)
        back.on_click = lambda e: self.window.show_view(MenuView())
        box.add(back)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(box, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(anchor)

    def start(self, level_id):
        self.window.show_view(MyGame(level_id))

    def on_draw(self):
        self.clear()
        self.ui.draw()

    def on_hide_view(self):
        self.ui.disable()