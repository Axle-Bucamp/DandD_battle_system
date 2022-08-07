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
    def __init__(self, call_on_generate=lambda: True, **kwargs):
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
        self.select_button = None

        self.title = "Load File "

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

        if "entities" in dict.keys() and "dead_list" in dict.keys() and "current_player" in dict.keys():
            battle_field.from_simple_json(dict)

        if "abilities" in dict.keys() or "effects" in dict.keys():
            Ability_manager.from_simple_json(dict)

        self.call_on_generate()
        self.dismiss()
