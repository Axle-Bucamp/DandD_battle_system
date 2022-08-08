from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


class popup_battle_draw(Popup):
    def __init__(self, title, action_name, list1=None, name1="", name2="", list2=None,
                 call=lambda selected1, all_selected2: True, with_description=False, default_description="", **kwargs):
        super().__init__(**kwargs)
        self.list1 = list1
        self.list2 = list2
        self.title = title
        self.choices = []

        self.name1 = name1
        self.name2 = name2
        self.selected1 = None
        self.selected2 = None

        self.all_selected2 = []

        colone = 1
        if self.list2 is not None:
            colone = 2

        container = GridLayout(cols=colone)
        layout = GridLayout(cols=1, size_hint=(None, 1), width=600)
        self.add_widget(container)
        adding = container

        if colone > 1:
            container.add_widget(layout)
            adding = layout
        self.description = TextInput(text=default_description, size_hint=(1, 1), readonly=True)

        if self.list1 is not None:
            self.button1, self.drop1 = self.draw_dropdown(self.list1, self.name1, False, with_description)
            adding.add_widget(self.button1)
            if with_description:
                adding.add_widget(self.description)

        if self.list2 is not None:
            self.button2, self.drop2 = self.draw_dropdown(self.list2, self.name2, True)
            adding.add_widget(self.button2)
            list_action = GridLayout(cols=2)
            plus_button = Button(text="add", size_hint=(1, None), height=50)
            list_action.add_widget(plus_button)
            minus_button = Button(text="remove", size_hint=(1, None), height=50)
            list_action.add_widget(minus_button)
            adding.add_widget(list_action)
            selected_options = GridLayout(cols=1)
            container.add_widget(selected_options)

            plus_button.bind(on_release=lambda x: [
                self.add_selected(selected_options)
            ])
            minus_button.bind(on_release=lambda x: {
                self.remove_selected(selected_options)
            })

        popup_action = GridLayout(rows=1, size_hint=(1, None), height=60)
        adding.add_widget(popup_action)
        action = Button(text=action_name, size_hint=(1, None), height=50)

        action.bind(on_release=lambda x: call(self.selected1, self.all_selected2))
        cancel = Button(text="Cancel", size_hint=(1, None), height=50)
        cancel.bind(on_release=lambda x: self.dismiss())

        popup_action.add_widget(action)
        popup_action.add_widget(cancel)

    def remove_selected(self, selected_options):
        if self.selected2 is not None:
            remove = None
            for child in selected_options.children:
                if child.value == self.selected2:
                    remove = child
            if remove is not None:
                selected_options.remove_widget(remove)
                self.all_selected2.remove(self.selected2)

    def add_selected(self, selected_options):
        if self.selected2 is not None:
            button_option = Button(text=self.selected2.name, size_hint=(1, None), height=50)
            button_option.bind(on_release=lambda x: selected_options.remove_widget(x))
            button_option.value = self.selected2
            self.all_selected2.append(self.selected2)
            selected_options.add_widget(button_option)

    def draw_dropdown(self, list_drop, default_name, is_multiple, with_description=False):
        x = DropDown()
        self.choices.append(x)
        x = self.choices.index(x)
        for elem in list_drop:
            btn = Button(text=elem.name, size_hint_y=None, height=60)
            btn.value = elem
            btn.bind(on_release=lambda btn_call: self.choices[x].select(btn_call))
            self.choices[x].add_widget(btn)
        select_button: Button = Button(text=default_name, size_hint=(1, None), height=50)
        select_button.value = None
        if is_multiple:
            self.choices[x].bind(on_select=lambda instance, values_selected: [
                setattr(select_button, 'value', values_selected.value),
                setattr(select_button, 'text', values_selected.text),
                self.set('selected2', values_selected.value)
            ])
        else:
            if with_description:
                self.choices[x].bind(on_select=lambda instance, value_selected: [
                    setattr(select_button, 'value', value_selected.value),
                    setattr(select_button, 'text', value_selected.text),
                    setattr(self.description, 'text', str(value_selected.value)),
                    self.set('selected1', value_selected.value)
                ])
            else:
                self.choices[x].bind(on_select=lambda instance, value_selected: [
                    setattr(select_button, 'value', value_selected.value),
                    setattr(select_button, 'text', value_selected.text),
                    self.set('selected1', value_selected.value)
                ])

        select_button.name = default_name
        select_button.bind(on_release=self.choices[x].open)

        return select_button, x

    def set(self, value, set_value):
        if value == "selected1":
            self.selected1 = set_value
        else:
            self.selected2 = set_value
