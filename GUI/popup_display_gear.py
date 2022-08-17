from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.label import Label
from GUI import popup_details_ability
from GUI import popup_battle_draw
from BattleSystem.Item_manager import Item_manager
from BattleSystem.BattleField import battle_field


class popup_display_gear(Popup):
    def __init__(self, entity, **kwargs):
        super().__init__(**kwargs)
        self.pop_ability = None
        self.size_hint = (None, None)
        self.size = (1600, 1000)
        self.title = "Inventory"
        self.entity = entity

        self.layout = GridLayout(cols=1)
        self.action_layout = GridLayout(cols=3, size_hint=(1, None), height=60)
        self.add_widget(self.layout)
        self.accor_item = Accordion(orientation='vertical')
        self.layout.add_widget(self.accor_item)

        self.draw_item_list(entity)

        loot_btn = Button(text="loot item")
        loot_btn.bind(on_release=lambda x: [self.loot_item_popup_open()])
        self.action_layout.add_widget(loot_btn)

        self.pop_loot = popup_battle_draw.popup_battle_draw(title="Loot Item",
                                                            action_name="Loot",
                                                            call=self.loot_item,
                                                            list1=Item_manager.gears,
                                                            name1="items")

        drop_btn = Button(text="drop item")
        drop_btn.bind(on_release=lambda x: [self.drop_item_popup_open()])
        self.action_layout.add_widget(drop_btn)

        self.pop_drop = popup_battle_draw.popup_battle_draw(title="Drop Item",
                                                            action_name="Drop",
                                                            call=self.drop_item,
                                                            list1=self.entity.gear,
                                                            name1="items")

        close_btn = Button(text="close")
        close_btn.bind(on_release=lambda x: [self.dismiss()])
        self.action_layout.add_widget(close_btn)

        self.layout.add_widget(self.action_layout)


    def drop_item_popup_open(self):
        self.pop_drop = popup_battle_draw.popup_battle_draw(title="Drop Item",
                                                            action_name="Drop",
                                                            call=self.drop_item,
                                                            list1=self.entity.gear,
                                                            name1="items")
        self.pop_drop.open()

    def loot_item_popup_open(self):
        self.pop_loot = popup_battle_draw.popup_battle_draw(title="Loot Item",
                                                            action_name="Loot",
                                                            call=self.loot_item,
                                                            list1=Item_manager.gears,
                                                            name1="items")
        self.pop_loot.open()

    def drop_item(self, selected1, selected2):
        if selected1 is not None:
            ind = battle_field.entities.index(self.entity)
            selected1.on_drop(battle_field.entities[ind])
        self.accor_item.clear_widgets()
        self.draw_item_list(self.entity)
        self.pop_drop.dismiss()

    def loot_item(self, selected1, selected2):
        if selected1 is not None:
            ind = battle_field.entities.index(self.entity)
            selected1.on_hold(battle_field.entities[ind])
        self.accor_item.clear_widgets()
        self.draw_item_list(self.entity)
        self.pop_loot.dismiss()

    def draw_item_list(self, entity):
        for item in entity.gear:
            type = int(item.is_consumable) + 1
            item_layout = AccordionItem(title=item.name,
                                        background_normal='images/acordeon/image_when_collapsed_party_'
                                              + str(type) + '.png')

            item_layout.add_widget(Label(text="[color=000000]" + item.description + "[/color]",
                                         markup=True, size_hint=(1, None), height=100))

            if type == 2:
                item_layout.add_widget(Label(text="[color=000000]" + str(item.nb_use) + "[/color]",
                                             markup=True, size_hint=(1, None), height=60))
            for key, bonus in item.charact_bonus.items():
                item_layout.add_widget(Label(text="[color=000000]" + str(key) + ": " + str(bonus) + "[/color]",
                                             markup=True, size_hint=(1, None), height=60))

            for ability in item.abilities:
                if ability in entity.ability:
                    ability_btn = Button(text="[color=000000]" + str(ability.name) + "[/color]",
                           markup=True, size_hint=(1, None), height=60)
                    ability_btn.value = ability
                    ability_btn.bind(on_press=self.get_detail)
                    item_layout.add_widget(ability_btn)

            self.accor_item.add_widget(item_layout)

    def get_detail(self, btn):
        self.pop_ability = popup_details_ability.popup_details_ability(btn.value)
        self.pop_ability.open()
