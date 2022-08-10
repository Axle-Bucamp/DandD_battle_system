from BattleSystem.BattleField import battle_field
from BattleSystem.Ability_manager import Ability_manager
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from GUI import player_turn
from GUI import mob_list
from GUI import party_member
from GUI import Main_window
from GUI import Action_menu
from kivy.config import Config
from GUI import popup_generation_battle
from GUI import popup_create_entity
from GUI import popup_load_json
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.lang.builder import Builder

Config.set('graphics', 'width', '2400')
Config.set('graphics', 'height', '1600')

Builder.load_file('UI_rules.kv')


class layout_colored(GridLayout):
    pass


class round_label_with_border(Label):
    pass


class round_box_with_border(GridLayout):
    pass


class Battle_application(App):
    container_app = GridLayout(cols=4, rows=1, size=(Window.width, Window.height))

    # color to use in the app design
    white_cream = get_color_from_hex("#F9EFEC")
    cream = get_color_from_hex("#F7C599")
    brown = get_color_from_hex("#ef9312")
    dark_brown = get_color_from_hex("#8A5546")

    # color used to design entity party
    sky_blue = get_color_from_hex("#8BCAFA")
    purple = get_color_from_hex("#8BCAFA")
    forest_green = get_color_from_hex("#5CFA72")
    yellow_dark = get_color_from_hex("#D6B22B")
    red = get_color_from_hex("#DB3425")
    dark_orange = get_color_from_hex("#F09900")
    green_yellow = get_color_from_hex("#D9D00B")
    black = get_color_from_hex("#00241F")
    gray_sky = get_color_from_hex("#008F7C")
    gray = get_color_from_hex("#7A8E82")

    party_color = [sky_blue, forest_green, yellow_dark, red, dark_orange, green_yellow, white_cream, black, gray_sky, gray]

    def build(self):
        self.draw_menu()
        self.battle = battle_field()
        self.title = "D&D Battle Management Tool"
        self.spell_manager = Ability_manager.basic()

        return self.container_app

    def draw_menu(self, btn=None):
        self.container_app.cols = 2
        self.container_app.clear_widgets()

        button_side = GridLayout(cols=1)
        self.container_app.add_widget(button_side)

        text_side = round_box_with_border(cols=1, rows=2, size_hint=(1, 1))
        self.container_app.add_widget(text_side)

        generate_entity = Button(text="[color=F59C4E][b]add character[/color][/b]",
                                 markup=True, size_hint=(1, None), height=80)
        generate_entity.background_color = get_color_from_hex("#ef9312")  # F7C599
        generate_battle = Button(text="[color=F59C4E][b]Generate Battle[/color][/b]",
                                 markup=True, size_hint=(1, None), height=80)
        generate_battle.background_color = get_color_from_hex("#ef9312")  # F7C599
        load_battle = Button(text="[color=F59C4E][b]Load file[/color][/b]",
                             markup=True, size_hint=(1, None), height=80)
        load_battle.background_color = get_color_from_hex("#ef9312")  # F7C599
        loading_file = popup_load_json.popup_load_json(call_on_generate=self.check_operationnal_battle)
        load_battle.bind(on_release=loading_file.open)
        self.join_battle = Button(text="[color=F59C4E][b]enter the Battlefield[/color][/b]",
                                  markup=True, size_hint=(1, None), height=80, disabled=True)
        self.join_battle.background_color = self.brown  # F7C599

        battle_generation = popup_generation_battle.popup_generation_battle(self.check_operationnal_battle)
        entity_generation = popup_create_entity.popup_create_entity(self.check_operationnal_battle)
        generate_entity.bind(on_release=entity_generation.open)
        generate_battle.bind(on_release=battle_generation.open)

        desc = round_label_with_border(text="[color=755E49][b]This is a battle game interface for D&D style game \n" +
                          "you can generate battle from basic setup \n" +
                          "or custom your own one. [/b][/color] \n \n" +
                          "[color=755E49][i] this tool is done to simplify battle for MJ online. \n" +
                          "be aware that You need to generate at least two \n" +
                          "party group to use this app.[/b][/color]",
                     markup=True, size_hint=(1, None), height=300
                     )

        text_side.add_widget(desc)

        self.battle_grid = GridLayout(cols=1)
        text_side.add_widget(self.battle_grid)

        self.join_battle.bind(on_release=self.draw_main_app)

        button_side.add_widget(Label(text="[color=755E49][b]D&D Battle System Tool[/b][/color]",
                                     markup=True))
        button_side.add_widget(generate_entity)
        button_side.add_widget(generate_battle)
        button_side.add_widget(load_battle)
        button_side.add_widget(self.join_battle)

    def check_operationnal_battle(self, btn=None):
        self.join_battle.disabled = True
        self.battle_grid.clear_widgets()
        y = self.battle.entities[0].party_id if self.battle.entities else 0
        for child in self.battle.entities:
            i = child.party_id
            if i != y:
                self.join_battle.disabled = False

            btn = Button(text=child.name + " " + child.description, size_hint=(1, None), height=50)
            btn.background_color = self.party_color[child.party_id -1]
            btn.value = child
            btn.bind(on_release=lambda x: [self.battle.entities.remove(x.value),
                                           self.battle_grid.remove_widget(x)])
            self.battle_grid.add_widget(btn)

    def draw_main_app(self, btn=None):
        if self.battle.current_player is None:
            self.battle.sort_init()

        self.container_app.cols = 4
        self.container_app.clear_widgets()

        self.container_app.add_widget(mob_list.mob_list())
        main_container = Main_window.Main_window(cols=1)
        main_container.size_hint = (2, 1)
        self.container_app.add_widget(main_container)
        main_container.add_widget(player_turn.player_turn())
        main_container.add_widget(party_member.party_member())
        action_panel = GridLayout(cols=1, size_hint=(None, 1), width=300)
        action_menu = Action_menu.Action_menu()
        action_panel.add_widget(action_menu)
        self.container_app.add_widget(action_panel)


if __name__ == '__main__':
    Battle_application().run()
