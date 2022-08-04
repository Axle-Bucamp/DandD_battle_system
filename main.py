from BattleSystem.BattleField import battle_field
from BattleSystem.Ability_manager import Ability_manager
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from GUI import player_turn
from GUI import mob_list
from GUI import party_member
from GUI import Main_window
from GUI import Action_menu
from kivy.config import Config

Config.set('graphics', 'width', '1800')
Config.set('graphics', 'height', '1000')


class Battle_application(App):

    def build(self):

        container_app = GridLayout(cols=4)
        container_app.add_widget(mob_list.mob_list())
        main_container = Main_window.Main_window(cols=1)
        main_container.size_hint = (2, 1)
        container_app.add_widget(main_container)
        main_container.add_widget(player_turn.player_turn())
        main_container.add_widget(party_member.party_member())
        action_panel = GridLayout(cols=1, size_hint=(None,1), width=300)
        action_menu = Action_menu.Action_menu()
        action_panel.add_widget(action_menu)
        container_app.add_widget(action_panel)

        return container_app




if __name__ == '__main__':
    battle = battle_field()
    spell_manager = Ability_manager.basic()
    battle.generate_group(nb_mob=2, mob_type=1, ilevel_to_fight=4, difficulty=1, party_id=0, name="wolf")
    battle.generate_group(nb_mob=3, mob_type=0, ilevel_to_fight=3, difficulty=1.2, party_id=1, name="bear")
    battle.generate_group(nb_mob=1, mob_type=2, ilevel_to_fight=2, difficulty=1.2, party_id=2, name="goblin caster")
    battle.sort_init()
    for entity in battle.entities:
        entity.learn_ability(spell_manager.abilities[0])

    Battle_application().run()
