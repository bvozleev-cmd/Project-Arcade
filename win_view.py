import arcade
import arcade.gui
import sounds
from level_select import LevelSelectView
from menu import MenuView

class WinView(arcade.View):
    def __init__(self, level_id, crystals, new_record=False):
        super().__init__()
        sounds.win.play()
        self.level_id = level_id
        self.crystals = crystals
        self.new_record = new_record
        self.ui = arcade.gui.UIManager()
        self.ui.enable()
        self.setup_ui()

    def setup_ui(self):
        box = arcade.gui.UIBoxLayout(space_between=20)

        title = arcade.gui.UILabel(
            text="УРОВЕНЬ ПРОЙДЕН!🎉",
            font_size=30,
            text_color=arcade.color.GOLD
        )
        box.add(title)

        if self.new_record:
            record = arcade.gui.UILabel(
                text="НОВЫЙ РЕКОРД!🦾",
                font_size=26,
                text_color=arcade.color.LIME
            )
            box.add(record)

        stats = arcade.gui.UILabel(
            text=f"💎: {self.crystals}",
            font_size=20,
            text_color=arcade.color.WHITE
        )
        box.add(stats)

        next_btn = arcade.gui.UIFlatButton(text="К выбору уровней", width=220)
        next_btn.on_click = lambda e: self.window.show_view(LevelSelectView())
        box.add(next_btn)

        menu_btn = arcade.gui.UIFlatButton(text="Главное меню", width=220)
        menu_btn.on_click = lambda e: self.window.show_view(MenuView())
        box.add(menu_btn)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(box, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(anchor)

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.AZURE)
        self.ui.draw()

    def on_hide_view(self):
        self.ui.disable()