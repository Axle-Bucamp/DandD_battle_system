from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from BattleSystem.Ability_manager import Ability_manager
from BattleSystem.Ability import Ability
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.switch import Switch


class popup_ability_creation(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (1200, 800)
        self.title = "Create ability"

        popup_main_grid = GridLayout(cols=1)
        self.add_widget(popup_main_grid)

        self.layout = GridLayout(cols=2)
        self.list_effects = GridLayout(cols=1)
        sep = GridLayout(cols=2)
        action = GridLayout(cols=3, size_hint=(1, None), height=50)

        sep.add_widget(self.layout)
        sep.add_widget(self.list_effects)
        popup_main_grid.add_widget(sep)
        popup_main_grid.add_widget(action)

        self.layout.add_widget(Label(text="Name:", size_hint_y=None, height=60))
        self.layout.add_widget(TextInput(size_hint_y=None, height=60))

        self.layout.add_widget(Label(text="Description:", size_hint_y=None, height=300))
        self.layout.add_widget(TextInput(size_hint_y=None, height=300))

        self.layout.add_widget(Label(text="Main only ability ?", size_hint_y=None, height=60))
        self.layout.add_widget(Switch(active=True, size_hint_y=None, height=60))

        self.layout.add_widget(Label(text="level:", size_hint_y=None, height=60))
        self.layout.add_widget(TextInput(size_hint_y=None, height=60))

        self.drop_effects = DropDown()
        for effect in Ability_manager.effects:
            btn = Button(text=effect.name, size_hint_y=None, height=60)
            btn.value = effect
            btn.bind(on_release=lambda btn_call: self.drop_effects.select(btn_call))
            self.drop_effects.add_widget(btn)

        select_button: Button = Button(text="add effect", size_hint=(1, None), height=50)
        select_button.bind(on_release=lambda x: [
            self.create_list_effect(),
            self.drop_effects.open(x)
        ])

        self.drop_effects.bind(on_select=self.add_effect)
        self.layout.add_widget(select_button)

        # cancel and validate button
        create = Button(text="Create")
        action.add_widget(create)
        create.bind(on_release=self.generate)

        cancel = Button(text="Cancel")
        action.add_widget(cancel)
        cancel.bind(on_release=self.dismiss)

    def add_effect(self, x, instance):
        effect_button = Button(text=instance.text, size_hint=(1, None), height=50)
        effect_button.value = instance.value
        effect_button.bind(on_release=lambda x: self.list_effects.remove_widget(x))
        self.list_effects.add_widget(effect_button)

    def generate(self, btn):
        name = self.layout.children[7].text
        description = self.layout.children[5].text
        principale = self.layout.children[3].active
        level = self.layout.children[1].text

        if level.isdigit():
            level = int(level)
        else:
            level = 1

        list_effect = []
        for child in self.list_effects.children:
            list_effect.append(child.value)

        add_abil = Ability(effects=list_effect, name=name,
                           description=description, is_principal=principale, level=level)
        Ability_manager.abilities.append(add_abil)
        self.dismiss()

    def create_list_effect(self):
        self.drop_effects.clear_widgets()
        for effect in Ability_manager.effects:
            btn = Button(text=effect.name, size_hint_y=None, height=60)
            btn.value = effect
            btn.bind(on_release=lambda btn_call: self.drop_effects.select(btn_call))
            self.drop_effects.add_widget(btn)
