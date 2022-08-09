from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from BattleSystem.Ability_manager import Ability_manager
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from BattleSystem.Buff_effect import Buff_effect
from BattleSystem.Dot_effect import Dot_effect
from BattleSystem.Effect import Effect
from BattleSystem.Dice import Dice
from kivy.uix.slider import Slider


class popup_effect_creation(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (1200, 800)
        self.title = "Create effect"
        self.generation_type = Effect
        self.caster_type = None
        self.resist_type = None
        self.dice = Dice.dice4

        popup_main_grid = GridLayout(cols=1)
        self.add_widget(popup_main_grid)

        choice_layout = GridLayout(cols=2, size_hint=(1, None), height=50)
        self.layout = GridLayout(cols=2)
        action = GridLayout(cols=3, size_hint=(1, None), height=50)
        popup_main_grid.add_widget(choice_layout)
        popup_main_grid.add_widget(self.layout)
        popup_main_grid.add_widget(action)

        self.drop_type = DropDown()
        name = ["instant damage", "damage over time", "boost", "curse"]
        for elem in range(len(name)):
            btn = Button(text=name[elem], size_hint_y=None, height=60)
            btn.value = elem
            btn.bind(on_release=lambda btn_call: self.drop_type.select(btn_call))
            self.drop_type.add_widget(btn)

        select_button: Button = Button(text="type of effect", size_hint=(1, None), height=50)
        select_button.bind(on_release=self.drop_type.open)
        self.drop_type.bind(on_select=lambda instance, values_selected: [
            self.draw_options(values_selected),
            setattr(select_button, 'text', values_selected.text)
                                                                         ])
        choice_layout.add_widget(select_button)

        # cancel and validate button
        cancel = Button(text="Create")
        action.add_widget(cancel)
        cancel.bind(on_release=self.generate)

        cancel = Button(text="Cancel")
        action.add_widget(cancel)
        cancel.bind(on_release=self.dismiss)

        self.drop_accuracy = DropDown()
        name = ["stre", "const", "dext", "char", "int", "None"]
        for elem in name:
            btn = Button(text=elem, size_hint_y=None, height=60)
            btn.value = elem
            btn.bind(on_release=lambda btn_call: self.drop_accuracy.select(btn_call.value))
            self.drop_accuracy.add_widget(btn)

        self.acc_button: Button = Button(text="accuracy type", size_hint=(1, None), height=50)
        self.acc_button.bind(on_release=self.drop_accuracy.open)
        self.drop_accuracy.bind(on_select=lambda instance, values_selected: self.set_accuracy(values_selected))

        self.drop_resistance = DropDown()
        name = ["stre", "const", "dext", "char", "int", "None"]
        for elem in name:
            btn = Button(text=elem, size_hint_y=None, height=60)
            btn.value = elem
            btn.bind(on_release=lambda btn_call: self.drop_resistance.select(btn_call.value))
            self.drop_resistance.add_widget(btn)

        self.resistance_button: Button = Button(text="resistance type", size_hint=(1, None), height=50)
        self.resistance_button.bind(on_release=self.drop_resistance.open)
        self.drop_resistance.bind(on_select=lambda instance, values_selected: self.set_resistance(values_selected))

        self.dice = DropDown()
        name = ["dice 4", "dice 6", "dice 8", "dice 12", "dice 20", "dice 100"]
        dice = [Dice.dice4, Dice.dice6, Dice.dice8, Dice.dice12, Dice.dice20, Dice.dice100]
        for elem in name:
            btn = Button(text=elem, size_hint_y=None, height=60)
            btn.value = dice[name.index(elem)]
            btn.name = elem
            btn.bind(on_release=lambda btn_call: self.dice.select(btn_call))
            self.dice.add_widget(btn)

        self.dice_button: Button = Button(text="damage dice", size_hint=(1, None), height=50)
        self.dice_button.bind(on_release=self.dice.open)
        self.dice.bind(on_select=lambda instance, values_selected: self.add_dice(values_selected))
        self.list_dice = GridLayout(cols=1)

        for child in self.layout.children:
            child.size_hint = (1, None)
            child.height = 60

    def draw_options(self, option):
        option = option.value
        for child in self.layout.children:
            child.clear_widgets()

        self.layout.clear_widgets()
        grid = GridLayout(cols=2)
        self.layout.add_widget(grid)
        self.layout.add_widget(self.list_dice)

        # name and desc
        grid.add_widget(Label(text="name"))
        grid.add_widget(TextInput())
        grid.add_widget(Label(text="description"))
        grid.add_widget(TextInput())

        # accuracy
        grid.add_widget(Label(text="caster accuracy stat"))
        grid.add_widget(self.acc_button)

        # resist
        grid.add_widget(Label(text="target resist stat"))
        grid.add_widget(self.resistance_button)

        # damage
        grid.add_widget(Label(text="cast power"))
        grid.add_widget(self.dice_button)

        # target
        grid.add_widget(Label(text="max AOE target"))
        grid.add_widget(TextInput())
        self.generation_type = Effect
        self.is_buff = True

        if option == 1:
            grid.add_widget(Label(text="duration"))
            grid.add_widget(Slider(min=1, max=10, value=1, step=1))
            self.generation_type = Dot_effect

        if option == 2:
            grid.add_widget(Label(text="duration"))
            grid.add_widget(Slider(min=1, max=10, value=1, step=1))
            self.generation_type = Buff_effect

        if option == 3:
            grid.add_widget(Label(text="duration"))
            grid.add_widget(Slider(min=1, max=10, value=1, step=1))
            self.generation_type = Buff_effect
            self.is_buff = False

    def add_dice(self, btn):
        button_dice = Button(text=btn.name, size_hint=(1, None), height=44)
        button_dice.value = btn.value
        button_dice.bind(on_release=lambda instance: self.list_dice.remove_widget(instance))
        self.list_dice.add_widget(button_dice)

    def set_resistance(self, value):
        self.resist_type = value
        if value == "None":
            self.resist_type = None
        self.resistance_button.text = value

    def set_accuracy(self, value):
        self.caster_type = value
        if value == "None":
            self.caster_type = None
        self.acc_button.text = value

    def generate(self, btn):
        dice = []
        for child in self.list_dice.children:
            dice.append(child.value)
        name = ""
        desc = ""
        aoe = 0
        i = 0
        turn_left = 0
        for child in self.layout.children[1].children:
            if isinstance(child, TextInput):
                if i == 2:
                    name = child.text
                if i == 1:
                    desc = child.text
                if i == 0:
                    if child.text.isdigit():
                        aoe = int(child.text)
                i += 1
            elif isinstance(child, Slider):
                turn_left = Slider.value

        effect = self.generation_type(scale_type=self.caster_type, resist_type=self.resist_type,
                                      damage=dice, name=name, description=desc, is_fixed_targeting=False,
                                      turn_left=turn_left, max_target=aoe)
        if not self.is_buff:
            effect.is_buff = self.is_buff

        Ability_manager.effects.append(effect)
        self.dismiss()
