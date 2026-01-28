import arcade
import arcade.gui
from resourses.code import sounds


class PauseView(arcade.View):
    def __init__(self, game_view):
        sounds.press_button_1.play()
        super().__init__()
        self.game_view = game_view
        self.ui = arcade.gui.UIManager()
        self.ui.enable()
        self.setup_ui()

    def setup_ui(self):
        box = arcade.gui.UIBoxLayout(space_between=20)
        title = arcade.gui.UILabel(
            text="ПАУЗА",
            font_size=30,
            text_color=arcade.color.GOLD,
            font_name=("Arial",)
        )
        box.add(title)

        continue_btn = arcade.gui.UIFlatButton(text="Продолжить", width=250)
        continue_btn.on_click = self.on_click_continue
        box.add(continue_btn)

        levels_btn = arcade.gui.UIFlatButton(text="Выбор уровня", width=250)
        levels_btn.on_click = self.on_click_levels
        box.add(levels_btn)

        menu_btn = arcade.gui.UIFlatButton(text="Главное меню", width=250)
        menu_btn.on_click = self.on_click_menu
        box.add(menu_btn)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(box, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(anchor)

    def on_click_continue(self, event):
        sounds.press_button_1.play()
        self.window.show_view(self.game_view)

    def on_click_levels(self, event):
        sounds.press_button_1.play()
        if self.game_view.level_select_view:
            self.game_view.level_select_view.back_view = self
            self.window.show_view(self.game_view.level_select_view)
        else:
            from resourses.code.level_select import LevelSelectView
            self.window.show_view(LevelSelectView(back_view=self))

    def on_click_menu(self, event):
        from resourses.code.menu import MenuView
        sounds.press_button_1.play()
        self.window.show_view(MenuView())

    def on_click_settings(self, event):
        sounds.press_button_1.play()
        print("Settings clicked from pause menu")

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.AZURE)
        self.ui.draw()

    def on_show_view(self):
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.on_click_continue(None)
