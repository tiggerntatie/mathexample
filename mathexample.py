# mathexample
import sys
sffloatpath = "https://tiggerntatie.github.io/sffloat/"
if sffloatpath not in sys.path:
    sys.path.append(sffloatpath)

from sffloat import sffloat, sqrt
from browser import window
from random import randint, seed
from ggame import App
from time import asctime, gmtime, now

"""
m = hashlib.md5("what is up dog".encode('utf-8'))

or

m = hashlib.sha256("what is up dog".encode('utf-8'))


>>> import base64
>>> base64.b64encode(m.digest())
b'gL+TIAkoFczEN0ZC4zlvbw=='
"""


class VectorMagnitudeExample(App):
    
    question = "Compute the magnitude of this vector: <{0},{1},{2}>."
    ID = "VM01"
    
    def __init__(self):
        self.answer = None
        self.paramsf = 2
        super().__init__()
        self.line = "start"
        #self.generateRandomQuestion()

    def generateRandomQuestion(self):
        seedtime = now()
        self.generateRandomParams(str(seedtime))


    def generateRandomParams(self, seedstr):
        self.timestamp = seedstr
        seed(int(seedstr))
        self.a = sffloat(randint(2,8), self.paramsf)
        self.b = sffloat(randint(2,8), self.paramsf)
        self.c = sffloat(randint(2,8), self.paramsf)
    
    @property
    def correctAnswer(self):
        return sqrt(self.a**2 + self.b**2 + self.c**2)
        
    def showQuestion(self):
        print(self.question.format(self.a, self.b, self.c))
        
    def getUserEmail(self):
        self.email = input("Enter your email name (without @hanovernorwichschools.org): ")
        
    def getUserAnswer(self):
        try:
            self.rawanswer = input("Enter your answer: ")
            self.answer = float(self.rawanswer)
        except ValueError:
            self.answer = None
        
    def showAnswer(self):
        print("Your answer is: ", self.answer)
        print("The correct answer is: ", self.correctAnswer)
        
    def userInteract(self):
        while not self.answer or not self.correctAnswer.equivalent_to_float(self.answer):
            self.generateRandomQuestion()
            self.showQuestion()
            self.getUserAnswer()
    
        self.actions = [
            self.generateRandomQuestion,
            self.showQuestion,
            self.getUserAnswer,
            self.showAnswer]
        self.x = 0

    def step(self):
        if self.line == "start":
            self.getUserEmail()
            self.line = "askquestion"
        elif self.line == "askquestion":
            self.generateRandomQuestion()
            self.showQuestion()
            self.line = "input"
        elif self.line == "input":
            self.getUserAnswer()
            if self.answer is None:
                self.line = "quit"
            elif self.correctAnswer.equivalent_to_float(self.answer):
                self.line = "correct"
            else:
                self.line = "incorrect"
            return
        elif self.line == "correct":
            print("Awesome! {0} is the correct answer.".format(self.correctAnswer))
            self.line = "finished"
        elif self.line == "incorrect":
            print("I'm sorry. You answered {0}.".format(self.answer))
            print("The correct answer is {0}.".format(self.correctAnswer))
            print("Try again!")
            self.line = "start"
        elif self.line == "quit":
            print("See you later!")
            self.line = "finished"
            

if __name__ == "__main__":
    myapp = VectorMagnitudeExample()
    myapp.run()
    #myapp.userInteract()
    
    