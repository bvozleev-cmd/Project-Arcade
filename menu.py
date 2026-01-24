import arcade
import arcade.gui
import sounds
from game import MyGame

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        sounds.press_button_1.play()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)
        start_button = arcade.gui.UIFlatButton(text="Начать игру", width=250)
        start_button.on_click = self.on_click_start
        self.v_box.add(start_button)
        settings_button = arcade.gui.UIFlatButton(text="Настройки", width=250)
        settings_button.on_click = self.on_click_settings
        self.v_box.add(settings_button)
        shop_button = arcade.gui.UIFlatButton(text="Магазин", width=250)
        from shop import ShopView
        shop_button.on_click = lambda e: self.window.show_view(ShopView())
        self.v_box.add(shop_button)
        quit_button = arcade.gui.UIFlatButton(text="Выход", width=250)
        quit_button.on_click = self.on_click_quit
        self.v_box.add(quit_button)
        anchor_layout = arcade.gui.UIAnchorLayout()
        anchor_layout.add(child=self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor_layout)
        self.title_text = arcade.Text(
            "Coin Quest",
            x=0,
            y=0,
            color=arcade.color.GOLD,
            font_size=80,
            anchor_x="center"
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AZURE)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_click_start(self, event):
        from level_select import LevelSelectView
        self.window.show_view(LevelSelectView(back_view=self))

    def on_click_settings(self, event):
        sounds.press_button_1.play()
        print("Settings clicked")

    def on_click_shop(self, event):
        sounds.press_button_1.play()
        print("Shop clicked")

    def on_click_quit(self, event):
        sounds.press_button_1.play()


    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.AZURE)
        self.title_text.x = self.window.width / 2
        self.title_text.y = self.window.height * 0.7
        self.title_text.draw()
        self.manager.draw()