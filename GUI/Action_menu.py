from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.accordion import Accordion, AccordionItem
from GUI import popup_generation_battle
from GUI import Main_window
from GUI import popup_create_entity
from GUI import popup_effect_creation


class Action_menu(Accordion):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        battle_management = AccordionItem(title="Battle")
        self.add_widget(battle_management)
        ability_management = AccordionItem(title="Ability")
        self.add_widget(ability_management)
        file_management = AccordionItem(title="File")
        self.add_widget(file_management)

        # drawing battle pannel :
        battle_options = GridLayout(cols=1)
        self.battle_delete_option = Button(text="remove entities", size_hint_y=None, height=44)
        battle_options.add_widget(self.battle_delete_option)

        self.battle_add_option = Button(text="create entity", size_hint_y=None, height=44)
        self.popup_create_entity = popup_create_entity.popup_create_entity(Main_window.refresh)
        self.battle_add_option.bind(on_press=self.popup_create_entity.open)
        battle_options.add_widget(self.battle_add_option)

        self.battle_generate_option = Button(text="generate entities", size_hint_y=None, height=44)
        self.pop_generation = popup_generation_battle.popup_generation_battle(Main_window.refresh)
        self.battle_generate_option.bind(on_press=self.pop_generation.open)
        battle_options.add_widget(self.battle_generate_option)

        self.battle_load_option = Button(text="load entities", size_hint_y=None, height=44)
        battle_options.add_widget(self.battle_load_option)

        battle_management.add_widget(battle_options)

        # drawing Ability pannel :
        ability_options = GridLayout(cols=1)
        self.ability_delete_option = Button(text="remove ability", size_hint_y=None, height=44)
        ability_options.add_widget(self.ability_delete_option)

        self.ability_create_option = Button(text="create ability", size_hint_y=None, height=44)
        ability_options.add_widget(self.ability_create_option)

        self.effect_create_option = Button(text="create effect", size_hint_y=None, height=44)
        self.popup_effect_creation = popup_effect_creation.popup_effect_creation(Main_window.refresh)
        self.effect_create_option.bind(on_press=self.popup_effect_creation.open)
        ability_options.add_widget(self.effect_create_option)

        self.ability_load_option = Button(text="load ability", size_hint_y=None, height=44)
        ability_options.add_widget(self.ability_load_option)

        ability_management.add_widget(ability_options)

        # drawing entity panel :
        # remove dot, buff, gear, ability
        # add buff, curse , gear, ability
        # update entity stats

        # drawing gear panel :
        # create
        # remove
        # load

        # drawing file pannel :
        file_options = GridLayout(cols=1)
        self.file_load_option = Button(text="load file", size_hint_y=None, height=44)
        file_options.add_widget(self.file_load_option)
        self.file_save_option = Button(text="save file", size_hint_y=None, height=44)
        file_options.add_widget(self.file_save_option)

        file_management.add_widget(file_options)
