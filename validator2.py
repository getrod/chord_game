from observer import *
import time
from my_socket import *
import json

# find a match in a list of ambigous chords
def chordMatch(questionChord: dict, answerChord: dict, useVoice = False):
    answer = None
    if answerChord['key'] == questionChord['key'] and \
        answerChord['type']['name'] == questionChord['type']['name']:
        if useVoice and 'voice' in answerChord and 'voice' in questionChord:
            if answerChord['voice'] == questionChord['voice'] \
                    and answerChord['voice']['details'] == questionChord['voice']['details']:
                return answerChord
        else: answer = answerChord
    return answer

def Score(question: dict, answer: dict, time: float):
    score = {
        'question': question,
        'answer': answer,
        'time': time
    }
    return score

class Validator():
    def __init__(self, compare_func, use_voice=False) -> None:
        self.questionState = False
        self.tic = 0
        self.toc = 0
        self.questionChord = None
        self.compare_func = compare_func
        self.use_voice = use_voice

    def set_question_chord(self, chord):
        self.questionState = True
        self.questionChord = chord
        # start a timer for how long it takes to respond to chord
        self.tic = time.perf_counter()

    def validate(self, chord_answer):
        if self.questionState:
            answer = self.compare_func(self.questionChord, chord_answer, self.use_voice)
            if answer:
                self.questionState = False
                self.toc = time.perf_counter()
                score = Score(self.questionChord, answer, self.toc-self.tic)
                return score
        return None
            



'''
Validator:
    - compare function 
    - set question chord
    - validate(answer) -> Score | None
        # compare answer to question chord



'''