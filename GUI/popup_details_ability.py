from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from BattleSystem.BattleField import battle_field
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label


class popup_details_ability(Popup):
    def __init__(self, ability, function=lambda: True, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (1200, 1000)
        self.title = ability.name
        self.ability = ability
        self.function = function

        popup_main_grid = GridLayout(cols=1)
        self.add_widget(popup_main_grid)

        self.layout = GridLayout(cols=1)
        action = GridLayout(cols=3, size_hint=(1, None), height=50)

        popup_main_grid.add_widget(self.layout)
        popup_main_grid.add_widget(action)

        self.layout.add_widget(Label(text=ability.name, size_hint=(1, None), height=50))
        self.layout.add_widget(Label(text=ability.description))

        self.effect_list = DropDown()
        for elem in ability.effects:
            btn = Button(text=elem.name, size_hint_y=None, height=60)
            btn.value = elem
            btn.bind(on_release=lambda btn_call: self.effect_list.select(btn_call.value))
            self.effect_list.add_widget(btn)

        self.button_choice: Button = Button(text="effect list", size_hint=(1, None), height=50)
        self.button_choice.bind(on_release=self.effect_list.open)
        self.effect_list.bind(on_select=lambda instance, values_selected: self.effect_detail(values_selected))
        self.layout.add_widget(self.button_choice)

        self.effect_description = Label(text="")
        self.layout.add_widget(self.effect_description)

        # cancel and validate button
        cancel = Button(text="remove")
        action.add_widget(cancel)
        cancel.bind(on_release=self.remove_ability)

        cancel = Button(text="close")
        action.add_widget(cancel)
        cancel.bind(on_release=self.dismiss)

    def effect_detail(self, values_selected):
        self.effect_description.text = str(values_selected)

    def remove_ability(self, btn):
        battle_field.current_player.ability.remove(self.ability)
        self.function()
        self.dismiss()
