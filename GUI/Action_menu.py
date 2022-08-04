from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.accordion import Accordion, AccordionItem
from GUI import popup_generation_battle
from kivy.app import App
from GUI import Main_window
class Action_menu(Accordion):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        app = App.get_running_app()

        battle_management = AccordionItem(title="Battle")
        self.add_widget(battle_management)
        ability_management = AccordionItem(title="Ability")
        self.add_widget(ability_management)
        file_management = AccordionItem(title="File")
        self.add_widget(file_management)

        # drawing battle pannel :
        battle_options = GridLayout(cols=1)
        battle_delete_option = Button(text="remove entities", size_hint_y=None, height=44)
        battle_options.add_widget(battle_delete_option)
        battle_add_option = Button(text="create entity", size_hint_y=None, height=44)
        battle_options.add_widget(battle_add_option)
        battle_generate_option = Button(text="generate entities", size_hint_y=None, height=44)
        pop = popup_generation_battle.popup_generation_battle(Main_window.refresh)
        battle_generate_option.bind(on_release=pop.open)
        battle_options.add_widget(battle_generate_option)
        battle_load_option = Button(text="load entities", size_hint_y=None, height=44)
        battle_options.add_widget(battle_load_option)

        battle_management.add_widget(battle_options)

        # drawing Ability pannel :
        ability_options = GridLayout(cols=1)
        ability_delete_option = Button(text="remove ability", size_hint_y=None, height=44)
        ability_options.add_widget(ability_delete_option)
        ability_create_option = Button(text="create ability", size_hint_y=None, height=44)
        ability_options.add_widget(ability_create_option)
        ability_load_option = Button(text="load ability", size_hint_y=None, height=44)
        ability_options.add_widget(ability_load_option)

        ability_management.add_widget(ability_options)

        # drawing Ability pannel :
        file_options = GridLayout(cols=1)
        file_load_option = Button(text="load file", size_hint_y=None, height=44)
        file_options.add_widget(file_load_option)
        file_save_option = Button(text="save file", size_hint_y=None, height=44)
        file_options.add_widget(file_save_option)

        file_management.add_widget(file_options)
