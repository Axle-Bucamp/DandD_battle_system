from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from BattleSystem.BattleField import battle_field
from BattleSystem.Effect import Effect
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from BattleSystem.Buff_effect import Buff_effect
from BattleSystem.Dot_effect import Dot_effect
from BattleSystem.Effect import Effect

class popup_effect_creation(Popup):
    def __init__(self, call_on_generate=lambda: True, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (1200, 800)
        self.title = "Create effect"
        self.call_on_generate = call_on_generate
        self.generaction_type = Effect

        popup_main_grid = GridLayout(cols=1)
        self.add_widget(popup_main_grid)

        choice_layout = GridLayout(cols=2)
        self.layout = GridLayout(cols=2)
        action = GridLayout(cols=3, size_hint=(1, None), height=50)
        popup_main_grid.add_widget(choice_layout)
        popup_main_grid.add_widget(self.layout)
        popup_main_grid.add_widget(action)

        self.drop_type = DropDown()
        name = ["damage", "dot", "buff"]
        for elem in range(3):
            btn = Button(text=name[elem], size_hint_y=None, height=60)
            btn.value = elem
            btn.bind(on_release=lambda btn_call: self.drop_type.select(btn_call))
            self.drop_type.add_widget(btn)

        select_button: Button = Button(text="type of entity", size_hint=(1, None), height=50)
        select_button.bind(on_release=self.drop_type.open)
        self.drop_type.bind(on_select=lambda instance, values_selected: self.draw_options(values_selected))
        choice_layout.add_widget(select_button)

        # cancel and validate button
        cancel = Button(text="Create")
        action.add_widget(cancel)
        cancel.bind(on_release=self.generate)

        cancel = Button(text="Cancel")
        action.add_widget(cancel)
        cancel.bind(on_release=self.dismiss)

        for child in self.layout.children:
            child.size_hint = (1, None)
            child.height = 60

    def draw_options(self, option):
        self.layout.clear_widgets()
        grid = GridLayout(cols=2)
        list_dice = GridLayout(cols=1)
        self.layout.add_widget(grid)
        self.layout.add_widget(list_dice)

        # name and desc
        grid.add_widget(Label(text="name"))
        grid.add_widget(TextInput())
        grid.add_widget(Label(text="description"))
        grid.add_widget(TextInput())

        # accuracy
        grid.add_widget(Label(text="caster accuracy stat"))
        # drop down

        # resist
        grid.layout.add_widget(Label(text="target resist stat"))
        # drop down

        # damage
        # multiple drop down
        grid.layout.add_widget(Label(text="damage dice"))

        # target
        grid.layout.add_widget(Label(text="max AOE target"))
        self.generaction_type = Effect

        if option == 1:
            grid.layout.add_widget(Label(text="duration"))
            self.generaction_type = Dot_effect

        if option == 2:
            grid.layout.add_widget(Label(text="duration"))
            grid.layout.add_widget(Label(text="buff stat"))
            self.generaction_type = Buff_effect
