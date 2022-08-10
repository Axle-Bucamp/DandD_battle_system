from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App


class end_battle_popup(Popup):
    def __init__(self, parti, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (1200, 800)
        self.title = "Well Played"

        popup_main_grid = GridLayout(cols=1)
        self.add_widget(popup_main_grid)
        popup_main_grid.add_widget(Label(text="Player from the party " + str(parti)
                                         + " \n have defeated all the other enemies"))

        app = App.get_running_app()
        btn_quit = Button(text="return to menu")
        btn_quit.bind(on_press=app.draw_menu)
        btn_quit.bind(on_release=self.dismiss)
        popup_main_grid.add_widget(btn_quit)
