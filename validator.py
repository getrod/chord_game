from observer import *
import time
from my_socket import *
import json

# find a match in a list of ambigous chords
def chordMatch(questionChord: dict, answers: dict, strict = False):
    answer = None
    for answerChord in answers:
        if answerChord['key'] == questionChord['key'] and \
            answerChord['type']['name'] == questionChord['type']['name']:
            if strict and 'voice' in answerChord and 'voice' in questionChord:
                if answerChord['voice'] != questionChord['voice'] \
                        and answerChord['voice']['details'] != questionChord['voice']['details']:
                    return None
            else: answer = answerChord
            break
    return answer

def Score(question: dict, answer: dict, time: float):
    score = {
        'question': question,
        'answer': answer,
        'time': time
    }
    return score

class Validator(Listener, Provider):
    def __init__(self) -> None:
        self.questionState = False
        self.tic = 0
        self.toc = 0
        self.questionChord = None
        self.answerChord = None
        super().__init__()

    def on_callback(self, message):
        respType, chord = message
        if respType == 'q':
            print('Question: ' + str(chord))
            # set the validator in a question state
            self.questionState = True
            self.questionChord = chord
            # start a timer for how long it takes to respond to chord
            self.tic = time.perf_counter()
        elif respType == 'a':
            chordAnswers = chord # confusing I know. a list of chords is returned for the answer message
            if self.questionState:
                self.answerChord = chordMatch(self.questionChord, chordAnswers)
                print('Answer: ' + str(self.answerChord))
                if self.answerChord:
                    self.questionState = False
                    self.toc = time.perf_counter()
                    score = Score(self.questionChord, self.answerChord, self.toc-self.tic)
                    sio.emit('on score', json.dumps(score, default=set_default))
                    self.update_listeners(score)

            # if in question state:
                # if chord matches question:
                    # reset question state
                    # stop timer
                    # emit "on score" to the web
                    # update listeners
                        # score database: save score some where
                        # question scheduler
            
