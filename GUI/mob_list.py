from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from BattleSystem.BattleField import battle_field
from kivy.uix.scrollview import ScrollView


class mob_list(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_scroll_y = True
        self.scroll_distance = 400
        root = Accordion()
        self.add_widget(root)
        if battle_field.current_player is not None:
            party_id = battle_field.current_player.party_id
        else:
            party_id = battle_field.entities[0].party_id

        root.orientation = 'vertical'
        ind = 0
        for entity in battle_field.entities:
            if entity.party_id != party_id:
                root.add_widget(self.draw_entity_stat(entity, ind))
                ind += 1
        root.size_hint = (1, None)
        root.height = ind * 100 + 350

    def draw_entity_stat(self, entity, ind):
        acc = AccordionItem(title=entity.name + " party : " + str(entity.party_id) + " init :" + str(ind))
        vbox = GridLayout(cols=1)
        vbox.entity = entity
        vbox.index = ind

        name = TextInput(text=entity.name, size_hint_y=None, height=50)
        name.var = entity.name
        name.var_name = "name"

        life = GridLayout(cols=5, size_hint_y=None, height=50)
        life.add_widget(Label(text=str(entity.hit_point) + "/" + str(entity.max_life), size_hint_x=None, width=200))
        life.add_widget(ProgressBar(max=entity.max_life, value=entity.hit_point))

        pushPlus = Button(text="+", size_hint_x=None, width=50)
        pushPlus.bind(on_press=self.change_life)
        life.add_widget(pushPlus)

        pushMinus = Button(text="-", size_hint_x=None, width=50)
        pushMinus.bind(on_press=self.change_life)
        life.add_widget(pushMinus)

        charac = self.charact_panel(entity)

        action = GridLayout(cols=2, size_hint_y=None, height=50)
        pushA = Button(text="manual change")
        pushA.bind(on_press=self.on_click_enable)

        action.add_widget(pushA)
        pushB = Button(text="submit", disabled=True)
        pushB.bind(on_press=self.on_click_submit)

        action.add_widget(pushB)

        vbox.add_widget(life)
        vbox.add_widget(charac)
        vbox.add_widget(action)
        acc.add_widget(vbox)

        return acc

    @staticmethod
    def charact_panel(entity):
        charac = GridLayout(cols=4, size_hint_y=None, height=200)
        charac.add_widget(Label(text="level :", size_hint_y=None, height=50))
        level = TextInput(text=str(entity.level), disabled=True, size_hint_y=None, height=50)
        level.var = entity.level
        level.var_name = "level"
        charac.add_widget(level)

        charac.add_widget(Label(text="Armor :", size_hint_y=None, height=50))
        armor_class = TextInput(text=str(entity.armor_class), disabled=True, size_hint_y=None, height=50)
        armor_class.var = entity.armor_class
        armor_class.var_name = "armor_class"
        charac.add_widget(armor_class)

        charac.add_widget(Label(text="Stren :", size_hint_y=None, height=50))
        strength = TextInput(text=str(entity.strength), disabled=True, size_hint_y=None, height=50)
        strength.var = entity.strength
        strength.var_name = "strength"
        charac.add_widget(strength)

        charac.add_widget(Label(text="Dext :", size_hint_y=None, height=50))
        agil = TextInput(text=str(entity.dexterity), disabled=True, size_hint_y=None, height=50)
        agil.var = entity.dexterity
        agil.var_name = "dexterity"
        charac.add_widget(agil)

        charac.add_widget(Label(text="Const :", size_hint_y=None, height=50))
        cons = TextInput(text=str(entity.constitution), disabled=True, size_hint_y=None, height=50)
        cons.var = entity.constitution
        cons.var_name = "constitution"
        charac.add_widget(cons)

        charac.add_widget(Label(text="Int :", size_hint_y=None, height=50))
        inte = TextInput(text=str(entity.intelligence), disabled=True, size_hint_y=None, height=50)
        inte.var = entity.intelligence
        inte.var_name = "intelligence"
        charac.add_widget(inte)

        charac.add_widget(Label(text="Char :", size_hint_y=None, height=50))
        char = TextInput(text=str(entity.charisma), disabled=True, size_hint_y=None, height=50)
        char.var = entity.charisma
        char.var_name = "charisma"
        charac.add_widget(char)

        return charac

    @staticmethod
    def on_click_enable(button):
        if button.text == "manual change":
            button.text = "cancel changes"
            for box in button.parent.parent.children:
                for child in box.children:
                    if isinstance(child, TextInput) or isinstance(child, Button):
                        child.disabled = False
        else:
            button.text = "manual change"
            for box in button.parent.parent.children:
                if isinstance(box, TextInput):
                    box.text = str(box.var)

                for child in box.children:
                    if isinstance(child, TextInput):
                        child.text = str(child.var)
                        child.disabled = True

                    if isinstance(child, Button):
                        if child.text == "submit":
                            child.disabled = True

    @staticmethod
    def on_click_submit(button):
        entity = button.parent.parent.entity
        for box in button.parent.parent.children:
            if isinstance(box, TextInput):
                box.var = box.text
                entity.name = box.var
            for child in box.children:
                if isinstance(child, TextInput):
                    if child.text.isdigit():
                        child.var = int(child.text)
                        if child.var_name != "armor_class" and child.var_name != "level":
                            entity.set_stat(child.var, child.var_name)
                        else:
                            if child.var_name != "armor_class":
                                entity.armor_class = child.var
                            else:
                                entity.level = child.var
                    else:
                        child.text = str(child.var)

    def change_life(self, button):
        entity = button.parent.parent.entity
        if button.text == "+":
            entity.hit_point += 1
        else:
            entity.hit_point -= 1
        for child in button.parent.children:
            if type(child) == type(ProgressBar()):
                child.value = entity.hit_point
            if type(child) == type(Label()):
                child.text = str(entity.hit_point) + "/" + str(entity.max_life)
