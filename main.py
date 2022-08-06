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

Config.set('graphics', 'width', '1800')
Config.set('graphics', 'height', '1000')


class Battle_application(App):
    container_app = GridLayout(cols=4)

    def build(self):
        self.draw_menu()
        self.battle = battle_field()
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
        join_battle = Button(text="enter the Battlefield", size_hint=(1, None), height=80)

        battle_generation = popup_generation_battle.popup_generation_battle()
        entity_generation = popup_create_entity.popup_create_entity()
        generate_entity.bind(on_release=entity_generation.open)
        generate_battle.bind(on_release=battle_generation.open)


        text_side.add_widget(Label(text="This is a battle game interface for D&D style game \n" +
                                                 "you can generate battle from basic setup \n" +
                                                 "or create your own one. \n" +
                                                 "this tool is done to simplify battle for MJ online. \n" +
                                                  "be aware that You need to generate at least two \n" +
                                                  " party group to use it."
                                            ))

        join_battle.bind(on_release=self.draw_main_app)

        button_side.add_widget(generate_entity)
        button_side.add_widget(generate_battle)
        button_side.add_widget(load_battle)
        button_side.add_widget(join_battle)

    def generate_battle(self, btn=None):
        self.battle.generate_group(nb_mob=2, mob_type=1, ilevel_to_fight=4, difficulty=1, party_id=0, name="wolf")
        self.battle.generate_group(nb_mob=3, mob_type=0, ilevel_to_fight=4, difficulty=1, party_id=1, name="goblin")
        for entity in self.battle.entities:
            entity.learn_ability(self.spell_manager.abilities[0])
        self.draw_main_app()

    def draw_main_app(self, btn=None):
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
