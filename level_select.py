import arcade
import arcade.gui
from database import get_levels
import sounds


class LevelSelectView(arcade.View):
    def __init__(self, back_view=None):
        super().__init__()
        self.back_view = back_view
        self.ui = arcade.gui.UIManager()
        self.ui.enable()
        sounds.press_button_1.play()
        box = arcade.gui.UIBoxLayout(space_between=15)

        for level_id, completed, crystals in get_levels():
            status = "✅" if completed else "❌"
            crystal_text = f" 💎 {crystals}/10" if completed else ""
            text = f"Уровень {level_id} {status}{crystal_text}"
            btn = arcade.gui.UIFlatButton(text=text, width=420)
            btn.on_click = lambda e, lvl=level_id: self.start(lvl)
            box.add(btn)

        back = arcade.gui.UIFlatButton(text="Назад", width=200)
        back.on_click = self.on_click_back
        box.add(back)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(box, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(anchor)

    def on_click_back(self, event):
        sounds.press_button_1.play()
        if self.back_view:
            self.window.show_view(self.back_view)
        else:
            from menu import MenuView
            self.window.show_view(MenuView())

    def start(self, level_id):
        from game import MyGame
        self.window.show_view(MyGame(level_id, level_select_view=self))

    def on_draw(self):
        self.clear()
        self.ui.draw()

    def on_show_view(self):
        self.ui.enable()
        arcade.set_background_color(arcade.color.AZURE)

    def on_hide_view(self):
        self.ui.disable()
