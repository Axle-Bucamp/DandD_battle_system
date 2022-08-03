from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from BattleSystem.BattleField import battle_field
from kivy.uix.progressbar import ProgressBar

class party_member(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        i = 0
        for entity in battle_field.entities:
            if entity.party_id == battle_field.current_player.party_id and entity != battle_field.current_player:
                self.add_widget(self.create_ally_panel(entity, i))
            i += 1
        self.cols = i

    def create_ally_panel(self, entity, index):
        ally_member = GridLayout(cols=1)
        ally_member.entity = entity

        life_box = GridLayout(size_hint_y=None, height=50)
        life_box.cols = 2
        life_box.add_widget(Label(text=str(entity.hit_point)
                                       + "/" + str(entity.max_life),
                                  size_hint_x=None, width=200))
        life_box.add_widget(ProgressBar(max=entity.max_life,
                                        value=entity.max_life))

        ally_member.add_widget(Label(text=entity.name + " " + str(index), size_hint_y=None, height=50))
        ally_member.add_widget(life_box)
        ally_member.add_widget(self.charact_panel(entity))


        return ally_member

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


