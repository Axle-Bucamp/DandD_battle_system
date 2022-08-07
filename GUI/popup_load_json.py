from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.core.window import Window
from BattleSystem.BattleField import battle_field
from BattleSystem.Entity import Entity
from BattleSystem.Ability import Ability
from BattleSystem.Ability_manager import Ability_manager
from BattleSystem.Effect import Effect
import json


class popup_load_json(Popup):
    def __init__(self, call_on_generate=lambda: True, type_init=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (600, 600)
        self.call_on_generate = call_on_generate
        popup_main_grid = GridLayout(cols=1)
        self.add_widget(popup_main_grid)
        layout = GridLayout(cols=1)
        action = GridLayout(cols=2, size_hint=(1, None), height=50)
        popup_main_grid.add_widget(layout)
        popup_main_grid.add_widget(action)
        self.drop_type = None
        self.type = "Battle"
        self.select_button = None

        if type_init is None:

            self.title = "Load File "
            self.drop_type = DropDown()
            name = ["Battle", "Ability"]
            for elem in name:
                btn = Button(text=elem, size_hint_y=None, height=60)
                btn.value = elem
                btn.bind(on_release=lambda btn_call: self.drop_type.select(btn_call))
                self.drop_type.add_widget(btn)

            self.select_button: Button = Button(text="type of entity", size_hint_y=None, height=60)
            self.select_button.bind(on_release=self.drop_type.open)
            self.drop_type.bind(on_select=self.change_type)
            layout.add_widget(self.select_button)
        else:

            self.type = type_init
            self.title = "Load " + str(type_init) + " File"

        self.file_btn = Button(text="Drag your file")
        layout.add_widget(self.file_btn)
        Window.bind(on_dropfile=self.handledrops)

    def change_type(self, btn, value):
        self.type = value.value
        self.select_button.text = value.value

    def handledrops(self, window_object, filename):
        try:
            with open(filename, "r") as jsonsave:
                dict = json.load(jsonsave)
        except:
            print(filename)
            print("file is not loaded")
            self.dismiss()

        self.file_btn.text = str(filename)

        if self.type == "Battle":
            battle_field.from_simple_json(dict)

        if self.type == "Ability":
            Ability_manager.from_simple_json(dict)

        self.call_on_generate()
        self.dismiss()
