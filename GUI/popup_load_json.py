from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from BattleSystem.BattleField import battle_field
from BattleSystem.Ability_manager import Ability_manager
from BattleSystem.Bestiary import Bestiary
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
                dictionary = json.load(jsonsave)
        except:
            print(filename)
            print("file is not loaded")
            self.dismiss()

        self.file_btn.text = str(filename)

        if "entities" in dictionary.keys() and\
                "dead_list" in dictionary.keys() and\
                "current_player" in dictionary.keys():
            battle_field.from_simple_json(dictionary)

        if "bestiary" in dictionary.keys():
            Bestiary.from_simple_json(dictionary)

        if "abilities" in dictionary.keys() or "effects" in dictionary.keys():
            Ability_manager.from_simple_json(dictionary)

        self.call_on_generate()
        self.dismiss()
