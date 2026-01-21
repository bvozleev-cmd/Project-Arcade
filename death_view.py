import arcade
import arcade.gui
from game import MyGame
from level_select import LevelSelectView


class DeathView(arcade.View):
    def __init__(self, level_id):
        super().__init__()
        self.level_id = level_id
        self.ui = arcade.gui.UIManager()
        self.ui.enable()

        box = arcade.gui.UIBoxLayout(space_between=20)

        restart = arcade.gui.UIFlatButton(text="Restart", width=300)
        restart.on_click = lambda e: self.window.show_view(MyGame(self.level_id))

        menu = arcade.gui.UIFlatButton(text="Level Menu", width=300)
        menu.on_click = lambda e: self.window.show_view(LevelSelectView())

        box.add(restart)
        box.add(menu)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(box, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(anchor)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "YOU DIED",
            self.window.width / 2,
            self.window.height * 0.7,
            arcade.color.RED,
            60,
            anchor_x="center"
        )
        self.ui.draw()

    def on_hide_view(self):
        self.ui.disable()