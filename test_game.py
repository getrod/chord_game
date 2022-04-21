'''

    REFERENCE

'''


import my_socket
import observer

# TODO: Make default_settings into an object and make that object serialized to json

namespace = '\\test'
default_settings = {}

class TestGameSettings:
    pass

class TestGame(observer.Listener):
    def __init__(self):
        
        @my_socket.sio.on('get question', namespace=namespace)
        def on_get_question(data):
            # generate and send the next question
            # ie. sio.emit('question', question)
            pass

        @my_socket.sio.on('get settings', namespace=namespace)
        def on_get_settings(data):
            # send settings
            # ie sio.emit('settings', settings)
            pass

        @my_socket.sio.on('get default settings', namespace=namespace)
        def on_get_default_settings(data):
            # get default settings
            # send default settings
            pass

        @my_socket.sio.on('change settings', namespace=namespace)
        def on_change_settings(data):
            # change the settings of this game
            pass
    
    # listen to chord messages
    def on_callback(self, chord):
        # send chord to validator
        # if valid 
            # emit score
            # wait for 1 second
            # send next question ie. emit("get question")
        pass


'''
Game {
    namespace: 'test'
    setting: {...}
}
'''