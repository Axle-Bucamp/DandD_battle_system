from kivy.uix.gridlayout import GridLayout
from GUI import player_turn
from GUI import party_member
from GUI import mob_list


class Main_window(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global refresh
        refresh = self.refresh_turn

    def refresh_turn(self):
        self.clear_widgets()
        self.add_widget(player_turn.player_turn())
        self.add_widget(party_member.party_member() )
        for child in self.parent.children:
            if isinstance(child, mob_list.mob_list):
                self.parent.remove_widget(child)
                self.parent.add_widget(mob_list.mob_list(), len(self.parent.children))
