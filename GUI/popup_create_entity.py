from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from BattleSystem.BattleField import battle_field
from BattleSystem.Entity import Entity
from kivy.uix.label import Label
from kivy.uix.slider import Slider


class popup_create_entity(Popup):
    def __init__(self, call_on_generate=lambda: True, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (600, 800)
        self.title = "Create entities"
        self.call_on_generate = call_on_generate

        popup_main_grid = GridLayout(cols=1)
        self.add_widget(popup_main_grid)

        layout = GridLayout(cols=2)
        action = GridLayout(cols=3, size_hint=(1, None), height=50)
        popup_main_grid.add_widget(layout)
        popup_main_grid.add_widget(action)

        # name
        layout.add_widget(Label(text="name :"))
        layout.add_widget(TextInput())

        # description
        layout.add_widget(Label(text="description :"))
        layout.add_widget(TextInput())

        # hit point
        layout.add_widget(Label(text="life point :"))
        layout.add_widget(TextInput())

        # class armor
        layout.add_widget(Label(text="class armor :"))
        layout.add_widget(Slider(min=1, max=20, value=1, step=1))

        # intelligence
        layout.add_widget(Label(text="intelligence :"))
        layout.add_widget(Slider(min=1, max=20, value=1, step=1))

        # charisma
        layout.add_widget(Label(text="charisma :"))
        layout.add_widget(Slider(min=1, max=20, value=1, step=1))

        # dexterity
        layout.add_widget(Label(text="dexterity :"))
        layout.add_widget(Slider(min=1, max=20, value=1, step=1))

        # strength
        layout.add_widget(Label(text="strength:"))
        layout.add_widget(Slider(min=1, max=20, value=1, step=1))

        # const
        layout.add_widget(Label(text="const :"))
        layout.add_widget(Slider(min=1, max=20, value=1, step=1))

        # ilevel
        layout.add_widget(Label(text="level :"))
        layout.add_widget(Slider(min=1, max=15, value=1, step=1))

        # party id
        layout.add_widget(Label(text="party id :"))
        layout.add_widget(Slider(min=1, max=10, value=1, step=1))

        self.quantity_on_select = Label(text="")
        action.add_widget(self.quantity_on_select)
        cancel = Button(text="create")
        action.add_widget(cancel)
        cancel.bind(on_release=self.create)

        cancel = Button(text="cancel")
        action.add_widget(cancel)
        cancel.bind(on_release=self.dismiss)

        for child in layout.children:
            child.size_hint = (1, None)
            child.height = 50
            if isinstance(child, Slider):
                child.bind(value=self.quantity_slide)

    def create(self, btn):
        party_id = btn.parent.parent.children[1].children[0].value
        lv = btn.parent.parent.children[1].children[2].value
        const = btn.parent.parent.children[1].children[4].value
        strength = btn.parent.parent.children[1].children[6].value
        dexterity = btn.parent.parent.children[1].children[8].value
        charisma = btn.parent.parent.children[1].children[10].value
        intelligence = btn.parent.parent.children[1].children[12].value
        armor_class = btn.parent.parent.children[1].children[14].value
        hit_point = btn.parent.parent.children[1].children[16].text

        if hit_point.isdigit():
            hit_point = int(hit_point)
        else:
            hit_point = 0

        description = btn.parent.parent.children[1].children[18].text
        name = btn.parent.parent.children[1].children[20].text
        entity = Entity(hit_point=hit_point, armor_class=armor_class, intelligence=intelligence, charisma=charisma,
                        dexterity=dexterity, strength=strength, constitution=const, ilevel=lv, gear=None,
                        ability=None, party_id=party_id, name=name, description=description)

        if entity.hit_point <= 0:
            entity.hit_point = entity.compute_health(lv, const)
            entity.max_life = entity.hit_point

        battle_field.entities.append(entity)
        self.call_on_generate()
        self.dismiss()

    def quantity_slide(self, slide, value):
        self.quantity_on_select.text = str(value)
