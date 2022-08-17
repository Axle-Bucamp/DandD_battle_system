from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from BattleSystem.Ability_manager import Ability_manager
from BattleSystem.Gear import Gear
from BattleSystem.Item_manager import Item_manager
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.switch import Switch


class popup_gear_creation(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (1200, 1200)
        self.title = "Smith a Gear"

        popup_main_grid = GridLayout(cols=1)
        self.add_widget(popup_main_grid)

        self.layout = GridLayout(cols=2)
        self.list_ability = GridLayout(cols=1)
        sep = GridLayout(cols=2)
        action = GridLayout(cols=3, size_hint=(1, None), height=50)

        sep.add_widget(self.layout)
        sep.add_widget(self.list_ability)
        popup_main_grid.add_widget(sep)
        popup_main_grid.add_widget(action)

        self.layout.add_widget(Label(text="Name:", size_hint_y=None, height=60))
        self.name = TextInput(size_hint_y=None, height=60)
        self.layout.add_widget(self.name)

        self.layout.add_widget(Label(text="Description:", size_hint_y=None, height=300))
        self.desc = TextInput(size_hint_y=None, height=300)
        self.layout.add_widget(self.desc )

        self.layout.add_widget(Label(text="consumable item ?", size_hint_y=None, height=60))
        self.consum = Switch(active=True, size_hint_y=None, height=60)
        self.layout.add_widget(self.consum)

        self.layout.add_widget(Label(text="number of use before fading:", size_hint_y=None, height=60))
        self.slide_usage = Slider(min=1, max=10, value=1, step=1)
        self.slide_usage.bind(value=self.set_slider_value)
        self.layout.add_widget(self.slide_usage)

        self.layout.add_widget(Label(text="give armor:", size_hint_y=None, height=60))
        self.slide_armor = Slider(min=-10, max=10, value=0, step=1)
        self.slide_armor.bind(value=self.set_slider_value)
        self.layout.add_widget(self.slide_armor)

        self.layout.add_widget(Label(text="give strength:", size_hint_y=None, height=60))
        self.slide_str = Slider(min=-10, max=10, value=0, step=1)
        self.slide_usage.bind(value=self.set_slider_value)
        self.layout.add_widget(self.slide_str)

        self.layout.add_widget(Label(text="give dexterity:", size_hint_y=None, height=60))
        self.slide_dext = Slider(min=-10, max=10, value=0, step=1)
        self.slide_dext.bind(value=self.set_slider_value)
        self.layout.add_widget(self.slide_dext)

        self.layout.add_widget(Label(text="give constitution:", size_hint_y=None, height=60))
        self.slide_const = Slider(min=-10, max=10, value=0, step=1)
        self.slide_const.bind(value=self.set_slider_value)
        self.layout.add_widget(self.slide_const)
        #
        self.layout.add_widget(Label(text="give int:", size_hint_y=None, height=60))
        self.slide_int = Slider(min=-10, max=10, value=0, step=1)
        self.slide_int.bind(value=self.set_slider_value)
        self.layout.add_widget(self.slide_int)

        self.layout.add_widget(Label(text="give wisdom:", size_hint_y=None, height=60))
        self.slide_wise = Slider(min=-10, max=10, value=0, step=1)
        self.slide_wise.bind(value=self.set_slider_value)
        self.layout.add_widget(self.slide_wise)

        self.layout.add_widget(Label(text="give charisma:", size_hint_y=None, height=60))
        self.slide_charisma = Slider(min=-10, max=10, value=0, step=1)
        self.slide_charisma.bind(value=self.set_slider_value)
        self.layout.add_widget(self.slide_charisma)

        self.value_display = Label(text="")
        self.layout.add_widget(self.value_display)

        self.drop_ability = DropDown()
        for ability in Ability_manager.abilities:
            btn = Button(text=ability.name, size_hint_y=None, height=60)
            btn.value = ability
            btn.bind(on_release=lambda btn_call: self.drop_ability.select(btn_call))
            self.drop_ability.add_widget(btn)

        select_button: Button = Button(text="add effect", size_hint=(1, None), height=50)
        select_button.bind(on_release=lambda x: [
            self.create_list_ability(),
            self.drop_ability.open(x)
        ])

        self.drop_ability.bind(on_select=self.add_ability)
        self.layout.add_widget(select_button)

        # cancel and validate button
        create = Button(text="Create")
        action.add_widget(create)
        create.bind(on_release=self.generate)

        cancel = Button(text="Cancel")
        action.add_widget(cancel)
        cancel.bind(on_release=self.dismiss)

    def set_slider_value(self, instance):
        self.value_display.text = instance.min + " < " + instance.value + " < " + instance.max

    def add_ability(self, x, instance):
        ability_button = Button(text=instance.text, size_hint=(1, None), height=50)
        ability_button.value = instance.value
        ability_button.bind(on_release=lambda x: self.list_ability.remove_widget(x))
        self.list_ability.add_widget(ability_button)

    def generate(self, btn):
        name = self.name.text
        description = self.desc.text
        consomable = self.consum.active
        nb_usage = self.slide_usage.value
        strength = self.slide_str.value
        dext = self.slide_dext.value
        const = self.slide_const.value
        wisd = self.slide_wise.value
        int = self.slide_int.value
        charisma = self.slide_charisma.value
        armor = self.slide_armor.value

        dict_bonus = {"stre": strength, "const": const, "dext": dext, "char": charisma, "int": int, "wisd": wisd, "armor_class": armor}

        list_ability = []
        for child in self.list_ability.children:
            list_ability.append(child.value)

        gear_smith = Gear(abilities=list_ability, name=name, description=description, is_consumable=consomable, nb_use=nb_usage, charact_bonus=dict_bonus)

        Item_manager.gears.append(gear_smith)
        self.dismiss()

    def create_list_ability(self):
        self.drop_ability.clear_widgets()
        for ability in Ability_manager.abilities:
            btn = Button(text=ability.name, size_hint_y=None, height=60)
            btn.value = ability
            btn.bind(on_release=lambda btn_call: self.drop_ability.select(btn_call))
            self.drop_ability.add_widget(btn)
