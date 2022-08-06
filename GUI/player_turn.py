from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from BattleSystem.BattleField import battle_field
from BattleSystem.Ability_manager import Ability_manager
from GUI import popup_details_ability
from GUI import popup_battle_draw


class player_turn(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.padding = 0.05
        # self.size_hint_y= 2

        self.pop = None
        self.ability_list_pop = None
        self.target = None
        self.ability = None

        self.add_widget(
            Label(text=battle_field.current_player.name + " party :" + str(
                battle_field.current_player.party_id) + " init :" + str(
                battle_field.entities.index(battle_field.current_player)), size_hint_y=None, height=50))

        life_box = GridLayout(size_hint_y=None, height=50)
        life_box.cols = 2
        life_box.add_widget(Label(text=str(battle_field.current_player.hit_point) + "/" +
                                  str(battle_field.current_player.max_life),
                                  size_hint_x=None, width=200))

        life_box.add_widget(ProgressBar(max=battle_field.current_player.max_life,
                                        value=battle_field.current_player.max_life))

        self.main_content = GridLayout(cols=2, rows=1)
        charac = self.charact_panel(battle_field.current_player)
        self.ability = self.ability_list(battle_field.current_player)

        self.main_content.add_widget(charac)
        self.main_content.add_widget(self.ability)

        action_button = self.action_widget(battle_field.current_player)

        self.add_widget(life_box)
        self.add_widget(self.main_content)
        self.add_widget(action_button)

    def update(self):
        self.parent.refresh_turn()

    def ability_list(self, entity):
        ability_list = GridLayout(cols=1)
        ability_list.add_widget(Label(text="ability :", size_hint_y=None, height=50))
        for ability in entity.ability:
            button_abil = Button(text=ability.name, size_hint_y=None, height=50)
            button_abil.value = ability
            button_abil.bind(on_release=self.draw_ability_details_popup)
            ability_list.add_widget(button_abil)

        add_abil_button = Button(text="Learn new ability", size_hint=(1, None), height=50)
        add_abil_button.bind(on_release=self.draw_choice_ability_popup)
        ability_list.add_widget(add_abil_button)

        return ability_list

    def draw_ability_details_popup(self, btn):
        popup_details = popup_details_ability.popup_details_ability(btn.value, self.refresh_ability)
        popup_details.open()

    def draw_choice_ability_popup(self, btn):
        list1 = Ability_manager.abilities
        func = self.learn_ability
        self.ability_list_pop = popup_battle_draw.popup_battle_draw(title="learn ability", action_name="learn",
                                                                    list1=list1,
                                                                    name1="Ability", name2=None, list2=None,
                                                                    call=func, with_description=True,
                                                                    default_description="choose one ability to "
                                                                                        "describe it")
        self.ability_list_pop.open()

    def learn_ability(self, selected1, selected2):
        battle_field.current_player.ability.append(selected1)
        self.ability_list_pop.dismiss()
        self.refresh_ability()

    def refresh_ability(self):
        self.main_content.remove_widget(self.ability)
        self.ability = self.ability_list(battle_field.current_player)
        self.main_content.add_widget(self.ability)

    def on_main_action(self, button):
        entity = button.parent.entity
        list1 = []
        list2 = []
        for ability in entity.ability:
            list1.append(ability)
        for entity in battle_field.entities:
            list2.append(entity)
        description = "you can only cast on the max target \n number of your wildest AOE effect \n" \
                      " rest will not be afflitected"
        self.pop = popup_battle_draw.popup_battle_draw(title="Main Action", action_name="Cast", list1=list1,
                                                       name1="Ability", name2="Target", list2=list2,
                                                       call=self.cast_primary, with_description=True,
                                                       default_description=description)
        self.pop.open()

    def on_second_action(self, button):
        entity = button.parent.entity
        list1 = []
        list2 = []
        for ability in entity.ability:
            if not ability.is_principal:
                list1.append(ability)
        for entity in battle_field.entities:
            list2.append(entity)
        description = "you can only cast on the max target number of your wildest AOE effect" \
                      " rest will not be afflitected"
        self.pop = popup_battle_draw.popup_battle_draw(title="Second Action", action_name="Cast", list1=list1,
                                                       name1="Ability", name2="Target",
                                                       list2=list2, call=self.cast_secondary,
                                                       with_description=True, default_description=description)
        self.pop.open()

    def action_widget(self, entity):
        action_list = GridLayout(cols=3, size_hint_y=None, height=50)
        action_list.entity = entity

        actionA = Button(text="main action")
        actionA.bind(on_press=self.on_main_action)
        action_list.add_widget(actionA)

        actionB = Button(text="second action")
        actionB.bind(on_press=self.on_second_action)
        action_list.add_widget(actionB)

        end_turn = Button(text="end turn")
        end_turn.bind(on_press=self.end_turn)
        action_list.add_widget(end_turn)
        return action_list

    def cast_primary(self, selected_ability, selected_target):
        if selected_ability is not None and len(selected_target) > 0:
            battle_field.current_player.main_action = selected_ability
            self.target = selected_target
            self.pop.dismiss()

    def cast_secondary(self, selected_ability, selected_target):
        if selected_ability is not None and len(selected_target) > 0:
            battle_field.current_player.second_action = selected_ability
            self.target = selected_target
            self.pop.dismiss()

    def end_turn(self, btn):
        if self.target is not None:
            if battle_field.current_player.main_action is not None:
                damage_done, resistance_target, accuracy_score = battle_field.current_player.cast_to_target(self.target,
                                                                                                            True)
            if battle_field.current_player.second_action is not None:
                damage_done, resistance_target, accuracy_score = battle_field.current_player.cast_to_target(self.target,
                                                                                                            False)
            # do animation for casting
        # do animation to end turn on win ...
        state, party_list = battle_field.end_turn()
        self.update()

    @staticmethod
    def charact_panel(entity):
        charac = GridLayout(cols=4)
        charac.add_widget(Label(text="level :"))
        level = TextInput(text=str(entity.level), disabled=True)
        level.var = entity.level
        level.var_name = "level"
        charac.add_widget(level)

        charac.add_widget(Label(text="Armor :"))
        armor_class = TextInput(text=str(entity.armor_class), disabled=True)
        armor_class.var = entity.armor_class
        armor_class.var_name = "armor_class"
        charac.add_widget(armor_class)

        charac.add_widget(Label(text="Stren :"))
        strength = TextInput(text=str(entity.strength), disabled=True)
        strength.var = entity.strength
        strength.var_name = "strength"
        charac.add_widget(strength)

        charac.add_widget(Label(text="Dext :"))
        agil = TextInput(text=str(entity.dexterity), disabled=True)
        agil.var = entity.dexterity
        agil.var_name = "dexterity"
        charac.add_widget(agil)

        charac.add_widget(Label(text="Const :"))
        cons = TextInput(text=str(entity.constitution), disabled=True)
        cons.var = entity.constitution
        cons.var_name = "constitution"
        charac.add_widget(cons)

        charac.add_widget(Label(text="Int :"))
        inte = TextInput(text=str(entity.intelligence), disabled=True)
        inte.var = entity.intelligence
        inte.var_name = "intelligence"
        charac.add_widget(inte)

        charac.add_widget(Label(text="Char :"))
        char = TextInput(text=str(entity.charisma), disabled=True)
        char.var = entity.charisma
        char.var_name = "charisma"
        charac.add_widget(char)

        for child in charac.children:
            child.size_hint_y = None
            child.height = 80

        return charac
