class Provider:
    def __init__(self):
        self.listeners = []

    def update_listeners(self, message):
        for listener in self.listeners:
            listener.on_callback(message)

    def subscribe(self, listener):
        self.listeners.append(listener)

    def callback(self, message):
        pass

    def listenersToString(self):
        s = 'Num listeners: ' + str(len(self.listeners)) + '\n'
        for listener in self.listeners:
            s += str(listener) + '\n'
        return s



class Listener:
    def on_callback(self, message):
        pass