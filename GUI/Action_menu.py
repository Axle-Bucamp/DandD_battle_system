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
from GUI import popup_gear_creation
from BattleSystem.BattleField import battle_field
from BattleSystem.Bestiary import Bestiary
from BattleSystem.Ability_manager import Ability_manager
from BattleSystem.Item_manager import Item_manager
from kivy.uix.popup import Popup
from BattleSystem.Dice import Dice
import json


class Action_menu(Accordion):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        battle_management = AccordionItem(title="Battle")
        self.add_widget(battle_management)
        bestiary = AccordionItem(title="Bestiary")
        self.add_widget(bestiary)
        ability_management = AccordionItem(title="Ability")
        self.add_widget(ability_management)
        item_management = AccordionItem(title="Item")
        self.add_widget(item_management)
        file_management = AccordionItem(title="File")
        self.add_widget(file_management)
        dice_management = AccordionItem(title="Dice")
        self.add_widget(dice_management)

        # drawing battle pannel :
        battle_options = GridLayout(cols=1)
        self.battle_delete_option = Button(text="remove entities", size_hint_y=None, height=44)

        self.loading_file = popup_load_json.popup_load_json()

        self.popup_remove_entity = popup_battle_draw.popup_battle_draw(title="Remove Entity",
                                                                       action_name="Remove",
                                                                       call=self.remove_entity,
                                                                       list1=battle_field.entities,
                                                                       name1="battler")

        self.battle_delete_option.bind(on_press=lambda x: [self.redraw_entity(), self.popup_remove_entity.open()])
        battle_options.add_widget(self.battle_delete_option)

        self.battle_add_option = Button(text="create entity", size_hint_y=None, height=44)
        self.popup_create_entity = popup_create_entity.popup_create_entity(Main_window.refresh)
        self.battle_add_option.bind(on_press=self.popup_create_entity.open)
        battle_options.add_widget(self.battle_add_option)

        self.battle_generate_option = Button(text="generate entities", size_hint_y=None, height=44)
        self.pop_generation = popup_generation_battle.popup_generation_battle(Main_window.refresh)
        self.battle_generate_option.bind(on_press=self.pop_generation.open)
        battle_options.add_widget(self.battle_generate_option)

        self.battle_resurection_option = Button(text="resurect entities", size_hint_y=None, height=44)
        self.popup_resurect = popup_battle_draw.popup_battle_draw(title="Graveyard", action_name="Rise from the dead",
                                                                  call=self.resurect_entity,
                                                                  list2=battle_field.dead_list, name2="death list")
        self.battle_resurection_option.bind(on_press=lambda x: [self.redraw_resurection(), self.popup_resurect.open()])
        battle_options.add_widget(self.battle_resurection_option)

        self.battle_load_option = Button(text="load entities", size_hint_y=None, height=44)
        self.battle_load_option.bind(on_press=self.loading_file.open)
        battle_options.add_widget(self.battle_load_option)

        self.battle_save_option = Button(text="save entities", size_hint_y=None, height=44)
        self.battle_save_option.bind(on_press=self.save_entities)
        battle_options.add_widget(self.battle_save_option)

        battle_management.add_widget(battle_options)

        # drawing bestiary options
        bestiary_options = GridLayout(cols=1)
        self.add_entity_to_bestiary = Button(text="add to bestiary", size_hint_y=None, height=44)
        self.popup_add_to_bestiary = popup_battle_draw.popup_battle_draw(title="Bestiary",
                                                                         action_name="add to bestiary",
                                                                         call=self.from_battle_to_bestiary,
                                                                         list2=battle_field.entities
                                                                               + battle_field.dead_list,
                                                                         name2="Choices")

        self.add_entity_to_bestiary.bind(on_press=lambda x: [self.refresh_bestiary_add_popup(),
                                                             self.popup_add_to_bestiary.open()])

        bestiary_options.add_widget(self.add_entity_to_bestiary)

        self.remove_entity_to_bestiary = Button(text="remove from bestiary", size_hint_y=None, height=44)
        self.popup_remove_from_bestiary = popup_battle_draw.popup_battle_draw(title="Bestiary",
                                                                              action_name="remove from bestiary",
                                                                              call=self.remove_from_bestiary,
                                                                              list2=Bestiary.bestiary, name2="Choices")

        self.remove_entity_to_bestiary.bind(on_press=lambda x: [self.refresh_bestiary_popup(),
                                                                self.popup_remove_from_bestiary.open()])

        bestiary_options.add_widget(self.remove_entity_to_bestiary)

        self.join_battle_from_bestiary_button = Button(text="join battle", size_hint_y=None, height=44)
        self.popup_join_from_bestiary = popup_battle_draw.popup_battle_draw(title="Bestiary",
                                                                            action_name="Join Battle",
                                                                            call=self.join_battle_from_bestiary,
                                                                            list2=Bestiary.bestiary, name2="Choices")
        self.join_battle_from_bestiary_button.bind(on_press=lambda x: [self.refresh_bestiary_to_battle_popup(),
                                                                       self.popup_join_from_bestiary.open()])
        bestiary_options.add_widget(self.join_battle_from_bestiary_button)

        self.save_entity_to_bestiary = Button(text="save bestiary", size_hint_y=None, height=44)
        self.save_entity_to_bestiary.bind(on_press=self.save_bestiary)
        bestiary_options.add_widget(self.save_entity_to_bestiary)

        self.load_entity_to_bestiary = Button(text="load bestiary", size_hint_y=None, height=44)
        self.load_entity_to_bestiary.bind(on_press=self.loading_file.open)
        bestiary_options.add_widget(self.load_entity_to_bestiary)

        bestiary.add_widget(bestiary_options)

        # drawing Ability pannel :
        ability_options = GridLayout(cols=1)
        self.ability_delete_option = Button(text="remove ability", size_hint_y=None, height=44)

        self.popup_remove_ability = popup_battle_draw.popup_battle_draw(title="Remove Ability", action_name="Remove",
                                                                        call=self.remove_ability, name1="ability list",
                                                                        list1=Ability_manager.abilities)

        self.ability_delete_option.bind(on_press=lambda x: [self.redraw_remove_ability(),
                                                            self.popup_remove_ability.open()])
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
        items_options = GridLayout(cols=1)
        self.items_loot_option = Button(text="Loot Item", size_hint_y=None, height=44)
        items_options.add_widget(self.items_loot_option)

        self.items_drop_option = Button(text="drop Item", size_hint_y=None, height=44)
        items_options.add_widget(self.items_drop_option)

        self.items_create_option = Button(text="Create Item", size_hint_y=None, height=44)
        self.popup_creation_item = popup_gear_creation.popup_gear_creation()
        self.items_create_option.bind(on_release=self.popup_creation_item.open)
        items_options.add_widget(self.items_create_option)

        self.items_remove_option = Button(text="Remove Item", size_hint_y=None, height=44)
        self.popup_remove_item = popup_battle_draw.popup_battle_draw(title="Remove item", action_name="Remove",
                                                                        call=self.remove_item, name1="item list",
                                                                        list1=Item_manager.gears)
        self.items_remove_option.bind(on_release=lambda x: [self.popup_remove_item_redraw(), self.popup_remove_item.open()])
        items_options.add_widget(self.items_remove_option)

        self.items_load_option = Button(text="Load Item", size_hint_y=None, height=44)
        self.items_load_option.bind(on_press=self.loading_file.open)
        items_options.add_widget(self.items_load_option)

        item_management.add_widget(items_options)

        # drawing file pannel :
        file_options = GridLayout(cols=1)

        self.file_load_option = Button(text="load file", size_hint_y=None, height=44)

        self.file_load_option.bind(on_press=self.loading_file.open)
        file_options.add_widget(self.file_load_option)

        self.file_save_option = Button(text="save file", size_hint_y=None, height=44)
        self.file_save_option.bind(on_press=self.save_files)
        file_options.add_widget(self.file_save_option)

        file_management.add_widget(file_options)

        # Dice management
        dice_options = GridLayout(cols=1)
        self.throw_4dice = Button(text="dice 4", size_hint_y=None, height=44)
        self.throw_4dice.bind(on_press=lambda x: self.popup_dice(4))
        dice_options.add_widget(self.throw_4dice)

        self.throw_6dice = Button(text="dice 6", size_hint_y=None, height=44)
        self.throw_6dice.bind(on_press=lambda x: self.popup_dice(6))
        dice_options.add_widget(self.throw_6dice)

        self.throw_8dice = Button(text="dice 8", size_hint_y=None, height=44)
        self.throw_8dice.bind(on_press=lambda x: self.popup_dice(8))
        dice_options.add_widget(self.throw_8dice)

        self.throw_12dice = Button(text="dice 12", size_hint_y=None, height=44)
        self.throw_12dice.bind(on_press=lambda x: self.popup_dice(12))
        dice_options.add_widget(self.throw_12dice)

        self.throw_20dice = Button(text="dice 20", size_hint_y=None, height=44)
        self.throw_20dice.bind(on_press=lambda x: self.popup_dice(20))
        dice_options.add_widget(self.throw_20dice)

        self.throw_100dice = Button(text="dice 100", size_hint_y=None, height=44)
        self.throw_100dice.bind(on_press=lambda x: self.popup_dice(100))
        dice_options.add_widget(self.throw_100dice)

        dice_management.add_widget(dice_options)

    def popup_remove_item_redraw(self):
        self.popup_remove_item = popup_battle_draw.popup_battle_draw(title="Remove item", action_name="Remove",
                                                                     call=self.remove_item, name1="item list",
                                                                     list1=Item_manager.gears)

    def remove_entity(self, select1, select2):
        if select1 is not None:
            battle_field.entities.remove(select1)
            Main_window.refresh()

        self.popup_remove_entity.dismiss()

    def remove_from_bestiary(self, select1, select2):
        for entity in select2:
            Bestiary.bestiary.remove(entity)

        self.popup_remove_from_bestiary.dismiss()

    def redraw_entity(self):
        self.popup_remove_entity = popup_battle_draw.popup_battle_draw(title="Remove Entity", action_name="Remove",
                                                                       call=self.remove_entity,
                                                                       list1=battle_field.entities)

    def refresh_bestiary_add_popup(self):
        self.popup_add_to_bestiary = popup_battle_draw.popup_battle_draw(title="Bestiary",
                                                                         action_name="add to bestiary",
                                                                         call=self.from_battle_to_bestiary,
                                                                         list2=battle_field.entities
                                                                               + battle_field.dead_list,
                                                                         name2="Choices")

    def join_battle_from_bestiary(self, select1, select2):
        for entity in select2:
            battle_field.entities.append(entity)
        Main_window.refresh()
        self.popup_join_from_bestiary.dismiss()

    def from_battle_to_bestiary(self, select1, select2):
        for entity in select2:
            Bestiary.bestiary.append(entity)

        self.popup_add_to_bestiary.dismiss()

    def refresh_bestiary_to_battle_popup(self):
        self.popup_join_from_bestiary = popup_battle_draw.popup_battle_draw(title="Bestiary",
                                                                            action_name="Join Battle",
                                                                            call=self.join_battle_from_bestiary,
                                                                            list2=Bestiary.bestiary, name2="Choices")

    def refresh_bestiary_popup(self):
        self.popup_remove_from_bestiary = popup_battle_draw.popup_battle_draw(title="Bestiary",
                                                                              action_name="remove from bestiary",
                                                                              call=self.remove_from_bestiary,
                                                                              list2=Bestiary.bestiary, name2="Choices")

    def redraw_resurection(self):
        self.popup_resurect = popup_battle_draw.popup_battle_draw(title="Graveyard", action_name="Rise from the dead",
                                                                  call=self.resurect_entity,
                                                                  list2=battle_field.dead_list, name2="death list")

    def redraw_remove_ability(self):
        self.popup_remove_ability = popup_battle_draw.popup_battle_draw(title="Remove Ability", action_name="Remove",
                                                                        call=self.remove_ability, name1="ability list",
                                                                        list1=Ability_manager.abilities)

    @staticmethod
    def popup_dice(res):
        pop = Popup(title="Dice " + str(res), size_hint=(None, None), size=(600, 600))
        layout = GridLayout(cols=1)
        pop.add_widget(layout)

        if res < 100:
            if res < 20:
                if res < 12:
                    if res < 8:
                        if res < 6:
                            dice = Dice.dice4()
                        else:
                            dice = Dice.dice6()
                    else:
                        dice = Dice.dice8()
                else:
                    dice = Dice.dice12()
            else:
                dice = Dice.dice20()
        else:
            dice = Dice.dice100()

        btn = Button(text=str(dice) + "/" + str(res))
        btn.bind(on_release=pop.dismiss)
        layout.add_widget(btn)
        pop.open()

    def remove_ability(self, select1, select2):
        Ability_manager.abilities.remove(select1)
        self.popup_remove_ability.dismiss()

    def resurect_entity(self, select1, select2):
        for row in select2:
            if select2 in battle_field.dead_list:
                row.hit_point = row.max_life
                if select1 is not None:
                    row.party_id = select1
                battle_field.entities.append(row)
                battle_field.dead_list.remove(row)

        Main_window.refresh()
        self.popup_resurect.dismiss()

    def save_abilities(self, btn):
        with open("Ability_list.json", "w") as outfile:
            json.dump(Ability_manager.to_simple_dict(Ability_manager), outfile)

    def save_entities(self, btn):
        with open("Battle.json", "w") as outfile:
            json.dump(battle_field.to_simple_dict(battle_field), outfile)

    def save_bestiary(self, btn):
        with open("Battle.json", "w") as outfile:
            json.dump(Bestiary.to_simple_dict(), outfile)

    def save_files(self, btn):
        with open("Battle.json", "w") as outfile:
            json.dump(battle_field.to_simple_dict(battle_field), outfile)

        with open("Ability_list.json", "w") as outfile:
            json.dump(Ability_manager.to_simple_dict(Ability_manager), outfile)

        with open("Battle.json", "w") as outfile:
            json.dump(Bestiary.to_simple_dict(), outfile)
