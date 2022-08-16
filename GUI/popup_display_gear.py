from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.label import Label
from GUI import popup_details_ability

class popup_gear_creation(Popup):
    def __init__(self, entity, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.size = (1600, 1000)
        self.title = "Inventory"

        popup_main_grid = GridLayout(cols=1)
        self.add_widget(popup_main_grid)

        self.layout = GridLayout(cols=1)
        self.accor_item = Accordion()
        self.layout.add_widget(self.accor_item)

        self.draw_item_list(entity)

        close_btn = Button(text="close")
        close_btn.bind(on_release=lambda x: [self.dismiss()])
        self.layout.add_widget(close_btn)


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
            for key, bonus in item.charact_bonus:
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
