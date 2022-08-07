from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.accordion import Accordion, AccordionItem
from GUI import popup_generation_battle
from GUI import Main_window
from GUI import popup_create_entity
from GUI import popup_effect_creation
from GUI import popup_ability_creation
from GUI import popup_battle_draw
from GUI import popup_load_json
from BattleSystem.BattleField import battle_field
from BattleSystem.Ability_manager import Ability_manager
import json

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

        self.loading_file = popup_load_json.popup_load_json()

        list1 = []
        for entity in battle_field.entities:
            if entity != battle_field.current_player:
                list1.append(entity)

        self.popup_remove_entity = popup_battle_draw.popup_battle_draw(title="Remove Entity", action_name="Remove",
                                                                       call=self.remove_entity, list1=list1)
        self.battle_delete_option.bind(on_press=self.popup_remove_entity.open)
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
        self.battle_load_option.bind(on_press=self.loading_file.open)
        battle_options.add_widget(self.battle_load_option)

        self.battle_save_option = Button(text="save entities", size_hint_y=None, height=44)
        self.battle_save_option.bind(on_press=self.save_entities)
        battle_options.add_widget(self.battle_save_option)

        battle_management.add_widget(battle_options)

        # drawing Ability pannel :
        ability_options = GridLayout(cols=1)
        self.ability_delete_option = Button(text="remove ability", size_hint_y=None, height=44)

        self.popup_remove_ability = popup_battle_draw.popup_battle_draw(title="Remove Ability", action_name="Remove",
                                                                        call=self.remove_ability,
                                                                        list1=Ability_manager.abilities)
        self.ability_delete_option.bind(on_press=self.popup_remove_ability.open)
        ability_options.add_widget(self.ability_delete_option)

        self.ability_create_option = Button(text="create ability", size_hint_y=None, height=44)
        self.popup_ability_creation = popup_ability_creation.popup_ability_creation()
        self.ability_create_option.bind(on_press=self.popup_ability_creation.open)
        ability_options.add_widget(self.ability_create_option)

        self.effect_create_option = Button(text="create effect", size_hint_y=None, height=44)
        self.popup_effect_creation = popup_effect_creation.popup_effect_creation()
        self.effect_create_option.bind(on_press=self.popup_effect_creation.open)
        ability_options.add_widget(self.effect_create_option)

        self.ability_load_option = Button(text="load ability", size_hint_y=None, height=44)
        self.ability_load_option.bind(on_press=self.loading_file.open)
        ability_options.add_widget(self.ability_load_option)

        self.ability_save_option = Button(text="save abilities", size_hint_y=None, height=44)
        self.ability_load_option.bind(on_press=self.save_abilities)
        ability_options.add_widget(self.ability_save_option)

        ability_management.add_widget(ability_options)

        # drawing gear panel :
        # create
        # remove
        # load

        # drawing file pannel :
        file_options = GridLayout(cols=1)

        self.file_load_option = Button(text="load file", size_hint_y=None, height=44)

        self.file_load_option.bind(on_press=self.loading_file_pop.open)
        file_options.add_widget(self.file_load_option)

        self.file_save_option = Button(text="save file", size_hint_y=None, height=44)
        self.file_save_option.bind(on_press=self.save_files)
        file_options.add_widget(self.file_save_option)

        file_management.add_widget(file_options)

    def remove_entity(self, select1, select2):
        if select1 is not None:
            battle_field.entities.remove(select1)
            Main_window.refresh()

        self.popup_remove_entity.dismiss()

    def remove_ability(self, select1, select2):
        Ability_manager.abilities.remove(select1)
        self.popup_remove_ability.dismiss()

    def save_abilities(self, btn):
        with open("Ability_list.json", "w") as outfile:
            json.dump(Ability_manager.to_simple_dict(Ability_manager), outfile)

    def save_entities(self, btn):
        with open("Battle.json", "w") as outfile:
            json.dump(battle_field.to_simple_dict(battle_field), outfile)

    def save_files(self, btn):
        with open("Battle.json", "w") as outfile:
            json.dump(battle_field.to_simple_dict(battle_field), outfile)

        with open("Ability_list.json", "w") as outfile:
            json.dump(Ability_manager.to_simple_dict(Ability_manager), outfile)
