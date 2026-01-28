import arcade
import arcade.gui

from resourses.code import sounds
from resourses.code.database import (
    get_skins,
    get_selected_skin,
    unlock_skin,
    select_skin,
    get_level_crystals
)
from resourses.code.menu import MenuView


class ShopView(arcade.View):
    def __init__(self):
        super().__init__()
        sounds.press_button_1.play()
        self.ui = arcade.gui.UIManager()
        self.ui.enable()
        self.skin_buttons = {}
        self.selected_skin = get_selected_skin()
        self.setup_ui()

    def setup_ui(self):
        self.ui.clear()
        self.skin_buttons.clear()
        total_crystals = sum(get_level_crystals(i) for i in range(1, 5))
        skins = get_skins()
        self.selected_skin = get_selected_skin()
        root = arcade.gui.UIBoxLayout(vertical=True, space_between=15)
        for idx, skin in enumerate(skins, start=1):
            skin_id, name, cost, unlocked = skin
            if not unlocked and total_crystals >= cost:
                unlock_skin(name)
                unlocked = True
            btn_text = f"Скин {idx}" if unlocked else f"Скин недоступен: {total_crystals} / {cost} 💎"
            btn = arcade.gui.UIFlatButton(text=btn_text, width=300)
            if unlocked:
                if name == self.selected_skin:
                    btn.normal_color = arcade.color.DARK_GREEN
                else:
                    btn.normal_color = arcade.color.GREEN
                btn.hover_color = arcade.color.APPLE_GREEN
                btn.pressed_color = arcade.color.DARK_PASTEL_GREEN
            else:
                btn.normal_color = arcade.color.DARK_GRAY
                btn.hover_color = arcade.color.GRAY
                btn.pressed_color = arcade.color.DIM_GRAY

            def on_click(e, skin_name=name, skin_cost=cost, skin_unlocked=unlocked):
                sounds.press_button_1.play()
                if skin_unlocked or total_crystals >= skin_cost:
                    if not skin_unlocked:
                        unlock_skin(skin_name)
                    select_skin(skin_name)
                    sounds.change_skin.play()
                    self.selected_skin = skin_name
                    self.update_buttons()

            btn.on_click = on_click
            self.skin_buttons[name] = btn
            root.add(btn)
        self.skin_label = arcade.gui.UILabel(
            text=f"Выбранный скин: {self.get_selected_skin_number()}",
            width=300,
            align="center",
            text_color=arcade.color.YELLOW,
            font_size=36
        )
        root.add(self.skin_label)
        root.add(arcade.gui.UISpace(height=10))
        back_btn = arcade.gui.UIFlatButton(text="Назад", width=300)
        back_btn.normal_color = arcade.color.LIGHT_GRAY
        back_btn.hover_color = arcade.color.SILVER
        back_btn.pressed_color = arcade.color.GRAY
        back_btn.on_click = lambda e: self.close_shop()
        root.add(back_btn)
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(root, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(anchor)

    def update_buttons(self):
        total_crystals = sum(get_level_crystals(i) for i in range(1, 5))
        skins = get_skins()
        for idx, (name, btn) in enumerate(self.skin_buttons.items(), start=1):
            unlocked_status = next(s[3] for s in skins if s[1] == name)
            cost = next(s[2] for s in skins if s[1] == name)
            if unlocked_status:
                btn.text = f"Скин {idx}"
            else:
                btn.text = f"Скин недоступен: {total_crystals} / {cost} 💎"
            if name == self.selected_skin:
                btn.normal_color = arcade.color.DARK_GREEN
            else:
                btn.normal_color = arcade.color.GREEN if unlocked_status else arcade.color.DARK_GRAY

    def close_shop(self):
        self.ui.disable()
        sounds.press_button_1.play()
        self.window.show_view(MenuView(win=1))

    def get_selected_skin_number(self):
        skins = get_skins()
        for idx, s in enumerate(skins, start=1):
            if s[1] == self.selected_skin:
                return f"Скин {idx}"
        return "нет"

    def on_draw(self):
        self.clear()
        self.skin_label.text = f"Выбранный скин: {self.get_selected_skin_number()}"
        self.ui.draw()
