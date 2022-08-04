from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from BattleSystem.BattleField import battle_field
from kivy.uix.label import Label
from kivy.uix.slider import Slider


class popup_generation_battle(Popup):
    def __init__(self, call_on_generate=lambda: True, **kwargs):
        super().__init__(**kwargs)
        self.call_on_generate = call_on_generate
        self.mob_type = 0
        popup_main_grid = GridLayout(cols=1)
        self.add_widget(popup_main_grid)
        layout = GridLayout(cols=2)
        action = GridLayout(cols=2, size_hint=(1, None), height=50)
        popup_main_grid.add_widget(layout)
        popup_main_grid.add_widget(action)

        layout.add_widget(Label(text="name :"))
        name_entity = TextInput()
        layout.add_widget(name_entity)

        layout.add_widget(Label(text="number :"))
        layout.add_widget(Label(text="level of the fight :"))
        number_of_attacker = Slider(min=0, max=10, value=1)
        layout.add_widget(number_of_attacker)
        ilevel = Slider(min=0, max=15, value=1)
        layout.add_widget(ilevel)

        layout.add_widget(Label(text="party id :"))
        party_id = Slider(min=0, max=10, value=1)
        layout.add_widget(party_id)

        # mob_type drop down
        self.drop_type = DropDown()
        name = ["barbare", "archer", "mage", "priest", "rogue", "paladin"]
        for elem in range(5):
            btn = Button(text=name[elem], size_hint_y=None, height=60)
            btn.value = elem
            btn.bind(on_release=lambda btn_call: self.drop_type.select(btn_call))
            self.drop_type.add_widget(btn)

        select_button: Button = Button(text="type of entity")
        select_button.bind(on_release=self.drop_type.open)
        self.drop_type.bind(on_select=lambda instance, values_selected: [
            setattr(select_button, 'value', values_selected.value),
            setattr(select_button, 'text', values_selected.text),
            self.set(values_selected.value)
        ])

        layout.add_widget(select_button)

        # cancel and validate button
        cancel = Button(text="generate")
        action.add_widget(cancel)
        cancel.bind(on_release=self.generate)

        cancel = Button(text="cancel")
        action.add_widget(cancel)
        cancel.bind(on_release=self.dismiss)

        for child in layout.children:
            child.size_hint = (1, None)
            child.height = 60

    def generate(self, btn):
        # for child in btn.parent.parent.children[1].children:
        #    print(child)
        name = btn.parent.parent.children[1].children[7].text
        nb = int(btn.parent.parent.children[1].children[4].value)
        lv = int(btn.parent.parent.children[1].children[3].value)
        party_id = int(btn.parent.parent.children[1].children[1].value)
        battle_field.generate_group(nb_mob=nb, mob_type=self.mob_type, ilevel_to_fight=lv,
                                    difficulty=1, party_id=party_id, name=name)
        self.call_on_generate()
        self.dismiss()

    def set(self, set_value):
        self.mob_type = set_value
