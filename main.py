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

Config.set('graphics', 'width', '2400')
Config.set('graphics', 'height', '1600')


class Battle_application(App):
    container_app = GridLayout(cols=4)

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
        text_side = GridLayout(cols=1)
        self.container_app.add_widget(text_side)

        generate_entity = Button(text="add character", size_hint=(1, None), height=80)
        generate_battle = Button(text="Generate Battle", size_hint=(1, None), height=80)
        load_battle = Button(text="Load file", size_hint=(1, None), height=80)
        loading_file = popup_load_json.popup_load_json(call_on_generate=self.check_operationnal_battle)
        load_battle.bind(on_release=loading_file.open)
        self.join_battle = Button(text="enter the Battlefield", size_hint=(1, None), height=80, disabled=True)

        battle_generation = popup_generation_battle.popup_generation_battle(self.check_operationnal_battle)
        entity_generation = popup_create_entity.popup_create_entity(self.check_operationnal_battle)
        generate_entity.bind(on_release=entity_generation.open)
        generate_battle.bind(on_release=battle_generation.open)

        text_side.add_widget(Label(text="This is a battle game interface for D&D style game \n" +
                                        "you can generate battle from basic setup \n" +
                                        "or custom your own one. \n \n" +
                                        "this tool is done to simplify battle for MJ online. \n" +
                                        "be aware that You need to generate at least two \n" +
                                        " party group to use this app.", size_hint=(1, None), height=300
                                   ))

        self.battle_grid = GridLayout(cols=1)
        text_side.add_widget(self.battle_grid)

        self.join_battle.bind(on_release=self.draw_main_app)

        button_side.add_widget(Label(text="D&D Battle System Tool"))
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

