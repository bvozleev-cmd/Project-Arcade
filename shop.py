from database import get_skins, get_selected_skin, unlock_skin, select_skin, get_level_crystals
from  menu import MenuView
import arcade
import arcade.gui

class ShopView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui = arcade.gui.UIManager()
        self.ui.enable()
        self.setup_ui()

    def setup_ui(self):
        box = arcade.gui.UIBoxLayout(space_between=20)
        total_crystals = sum([get_level_crystals(i) for i in range(1, 6)])

        self.skins = get_skins()
        selected = get_selected_skin()

        for skin in self.skins:
            skin_id, name, cost, unlocked = skin

            # Иконка скина
            try:
                texture = arcade.load_texture(f"images/characters/{name}.png")
            except:
                texture = arcade.make_soft_square_texture(64, arcade.color.GRAY, outer_alpha=255)

            btn = arcade.gui.UITextureButton(texture=texture, width=64, height=64)

            # Добавляем прогресс под иконкой, если не разблокирован
            if not unlocked:
                progress_text = f"{min(total_crystals, cost)}/{cost} 💎"
                label = arcade.gui.UILabel(text=progress_text, font_size=14, text_color=arcade.color.WHITE)
                box.add(label)

            # Клик на скин
            def on_click(e, skin_name=name, skin_cost=cost, skin_unlocked=unlocked):
                if skin_unlocked or total_crystals >= skin_cost:
                    if not skin_unlocked:
                        unlock_skin(skin_name)
                    select_skin(skin_name)
                    print(f"Выбран скин: {skin_name}")
                    self.window.show_view(LevelSelectView())  # Возврат в выбор уровня

            btn.on_click = on_click
            box.add(btn)

        back_btn = arcade.gui.UIFlatButton(text="Назад", width=200)
        back_btn.on_click = lambda e: self.window.show_view(MenuView())
        box.add(back_btn)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(box, anchor_x="center_x", anchor_y="center_y")
        self.ui.add(anchor)

    def on_draw(self):
        self.clear()
        self.ui.draw()