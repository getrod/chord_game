from observer import Provider

class MidiProvider(Provider):
    is_registered = False
    def __init__(self, port = "No Port"):
        self.port = port
        super().__init__()

    '''Send listeners latest midi message'''
    def callback(self, message):
        self.update_listeners(message)

    def register_midiin(self, midiin, port_name):
        if self.is_registered == False:
            self.port = port_name
            midiin.set_callback(self)
            self.is_registered = True

    def __call__(self, event, data=None):
        message, deltatime = event
        self.callback(message)
    

midi_provider = MidiProvider()