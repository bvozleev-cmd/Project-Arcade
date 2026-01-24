import arcade
import arcade.gui
from database import get_skins, get_selected_skin, unlock_skin, select_skin, get_level_crystals
from menu import MenuView


class ShopView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui = arcade.gui.UIManager()
        self.ui.enable()
        self.skin_buttons = {}
        self.setup_ui()

    def setup_ui(self):
        self.ui.clear()
        self.skin_buttons.clear()
        total_crystals = sum(get_level_crystals(i) for i in range(1, 6))
        skins = get_skins()
        selected_skin = get_selected_skin()
        root = arcade.gui.UIBoxLayout(vertical=True, space_between=15)
        for idx, skin in enumerate(skins, start=1):
            skin_id, name, cost, unlocked = skin
            if unlocked:
                btn_color = arcade.color.GREEN
                btn_text = f"Скин {idx}"
            else:
                btn_color = arcade.color.DARK_GRAY
                btn_text = f"Закрыт (стоимость: {cost} 💎)"
            btn = arcade.gui.UIFlatButton(text=btn_text, width=300)
            btn.normal_color = btn_color
            btn.hover_color = arcade.color.LIGHT_GRAY

            def on_click(e, skin_name=name, skin_cost=cost, skin_unlocked=unlocked):
                if skin_unlocked or total_crystals >= skin_cost:
                    if not skin_unlocked:
                        unlock_skin(skin_name)
                    select_skin(skin_name)
                    self.window.show_view(ShopView())  # Перерисовка магазина

            btn.on_click = on_click
            self.skin_buttons[name] = btn
            root.add(btn)
            if name == selected_skin:
                btn.border_width = 3
                btn.border_color = arcade.color.YELLOW  # выделяем рамкой выбранный скин
        back_btn = arcade.gui.UIFlatButton(text="Назад", width=300)
        back_btn.on_click = lambda e: self.window.show_view(MenuView())
        root.add(back_btn)
        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(root, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(anchor)

    def on_draw(self):
        self.clear()
        self.ui.draw()
