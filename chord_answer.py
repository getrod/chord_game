from observer import *

class ChordAnswer(Listener, Provider):
    def on_callback(self, chord):
        self.update_listeners(('a', chord)) # validator is sent this