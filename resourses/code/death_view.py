import arcade
import arcade.gui
from game import MyGame
from level_select import LevelSelectView
import sounds


class DeathView(arcade.View):
    def __init__(self, level_id):
        super().__init__()
        self.level_id = level_id
        self.ui = arcade.gui.UIManager()
        self.ui.enable()
        sounds.game_over.play()
        box = arcade.gui.UIBoxLayout(space_between=20)

        restart = arcade.gui.UIFlatButton(text="Начать сначала", width=300)
        restart.on_click = lambda e: self.window.show_view(MyGame(self.level_id))

        menu = arcade.gui.UIFlatButton(text="Меню уровней", width=300)
        menu.on_click = lambda e: self.window.show_view(LevelSelectView())

        box.add(restart)
        box.add(menu)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(box, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(anchor)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "ВЫ ПРОИГРАЛИ!😿",
            self.window.width / 2,
            self.window.height * 0.7,
            arcade.color.YELLOW,
            60,
            anchor_x="center"
        )
        self.ui.draw()

    def on_hide_view(self):
        self.ui.disable()