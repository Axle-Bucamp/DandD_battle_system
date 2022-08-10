from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from BattleSystem.BattleField import battle_field
from BattleSystem.Ability_manager import Ability_manager
from GUI import popup_details_ability
from GUI import popup_battle_draw
from GUI import end_battle_popup
from kivy.utils import get_color_from_hex


class ability_list_layout(GridLayout):
    pass


class player_turn(GridLayout):
    # color to use in the app design
    white_cream = get_color_from_hex("#F9EFEC")
    cream = get_color_from_hex("#F7C599")
    brown = get_color_from_hex("#ef9312")
    dark_brown = get_color_from_hex("#8A5546")
    wood = get_color_from_hex("#5A3300")

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

    party_color = [sky_blue, forest_green, yellow_dark,
                   red, dark_orange, green_yellow,
                   white_cream, black, gray_sky, gray]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.padding = 0.05
        # self.size_hint_y= 2

        self.pop = None
        self.ability_list_pop = None
        self.target = None
        self.ability = None

        name_button = Button(text="[b]current player : " + battle_field.current_player.name + "[/b]",
                             markup=True, size_hint_y=None, height=50)
        name_button.background_color = self.party_color[battle_field.current_player.party_id - 1]
        self.add_widget(name_button)

        life_box = GridLayout(size_hint_y=None, height=50)
        life_box.cols = 2
        life_box.add_widget(Label(text="[color=000000][b]" + str(battle_field.current_player.hit_point) + "/" +
                                  str(battle_field.current_player.max_life) + "[/color][/b]", markup=True,
                                  size_hint_x=None, width=200))

        life_box.add_widget(ProgressBar(max=battle_field.current_player.max_life,
                                        value=battle_field.current_player.max_life))

        self.main_content = GridLayout(cols=2, rows=1)
        charac = self.charact_panel(battle_field.current_player)
        self.ability, self.ability_learn = self.ability_list(battle_field.current_player)

        self.main_content.add_widget(charac)
        ability_older = GridLayout(rows=2)
        ability_older.add_widget(self.ability)
        ability_older.add_widget(self.ability_learn)
        self.main_content.add_widget(ability_older)

        action_button = self.action_widget(battle_field.current_player)

        self.add_widget(life_box)
        self.add_widget(self.main_content)
        self.add_widget(action_button)

    def update(self):
        self.parent.refresh_turn()

    def ability_list(self, entity):
        ability_list = ability_list_layout(cols=1)

        ability_list.add_widget(Label(text="[color=000000][b]abilities :[/color][/b]",
                                      markup=True, size_hint_y=None, height=50))
        for ability in entity.ability:
            button_abil = Button(text=ability.name, size_hint_y=None, height=50)
            button_abil.value = ability
            button_abil.bind(on_release=self.draw_ability_details_popup)
            ability_list.add_widget(button_abil)

        add_abil_button = Button(text="Learn new ability", size_hint=(1, None), height=50)
        add_abil_button.background_color = self.purple
        add_abil_button.bind(on_release=self.draw_choice_ability_popup)

        return ability_list, add_abil_button

    def draw_ability_details_popup(self, btn):
        popup_details = popup_details_ability.popup_details_ability(btn.value, self.refresh_ability)
        popup_details.open()

    def draw_choice_ability_popup(self, btn):
        list1 = []
        for ability in Ability_manager.abilities:
            if ability.level <= battle_field.current_player.level:
                list1.append(ability)

        func = self.learn_ability
        self.ability_list_pop = popup_battle_draw.popup_battle_draw(title="learn ability", action_name="learn",
                                                                    list1=list1,
                                                                    name1="Ability", name2=None, list2=None,
                                                                    call=func, with_description=True,
                                                                    default_description="choose one ability to "
                                                                                        "describe it")
        self.ability_list_pop.open()

    def learn_ability(self, selected1, selected2):
        if selected1 is not None:
            battle_field.current_player.ability.append(selected1)
            self.ability_list_pop.dismiss()
            self.refresh_ability()

    def refresh_ability(self):
        self.main_content.remove_widget(self.ability)
        self.ability, self.abil_learning = self.ability_list(battle_field.current_player)
        ability_older = GridLayout(rows=2)
        ability_older.add_widget(self.ability)
        ability_older.add_widget(self.abil_learning)
        self.main_content.add_widget(ability_older)

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
        if not state:
            pop_end = end_battle_popup.end_battle_popup(party_list)
            pop_end.open()
        # do a popup to return to menu and display victorious party
        self.update()

    @staticmethod
    def charact_panel(entity):
        charac = GridLayout(cols=4)
        charac.add_widget(Label(text="[color=000000][b]level :[/color][/b]", markup=True))
        level = TextInput(text=str(entity.level), disabled=True)
        level.var = entity.level
        level.var_name = "level"
        charac.add_widget(level)

        charac.add_widget(Label(text="[color=000000][b]Armor :[/color][/b]", markup=True))
        armor_class = TextInput(text=str(entity.armor_class), disabled=True)
        armor_class.var = entity.armor_class
        armor_class.var_name = "armor_class"
        charac.add_widget(armor_class)

        charac.add_widget(Label(text="[color=DB2F1C][b]Stren :[/color][/b]", markup=True))
        strength = TextInput(text=str(entity.strength), disabled=True)
        strength.var = entity.strength
        strength.var_name = "strength"
        charac.add_widget(strength)

        charac.add_widget(Label(text="[color=0BA808][b]Dext :[/color][/b]", markup=True))
        agil = TextInput(text=str(entity.dexterity), disabled=True)
        agil.var = entity.dexterity
        agil.var_name = "dexterity"
        charac.add_widget(agil)

        charac.add_widget(Label(text="[color=3636FF][b]Const :[/color][/b]", markup=True))
        cons = TextInput(text=str(entity.constitution), disabled=True)
        cons.var = entity.constitution
        cons.var_name = "constitution"
        charac.add_widget(cons)

        charac.add_widget(Label(text="[color=F0028D][b]Int :[/color][/b]", markup=True))
        inte = TextInput(text=str(entity.intelligence), disabled=True)
        inte.var = entity.intelligence
        inte.var_name = "intelligence"
        charac.add_widget(inte)

        charac.add_widget(Label(text="[color=DB8B27][b][color=DB8B27][b]Char :[/color][/b]", markup=True))
        char = TextInput(text=str(entity.charisma), disabled=True)
        char.var = entity.charisma
        char.var_name = "charisma"
        charac.add_widget(char)

        for child in charac.children:
            child.size_hint_y = None
            child.height = 80

        return charac
