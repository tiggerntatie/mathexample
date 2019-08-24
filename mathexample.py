# mathexample
import sys
import hashlib
import base64
imports = [
    "https://tiggerntatie.github.io/sffloat/",
    ]
for path in imports:
    if path not in sys.path:
        sys.path.append(path)

from sffloat import sffloat, sqrt
from browser import window
from random import randint, seed
from ggame import App
from time import asctime, gmtime, now


class VectorMagnitudeExample(App):
    
    question = "Compute the magnitude of this vector: <{0},{1},{2}>."
    ID = "VM01"
    
    def __init__(self):
        self.answer = None
        self.paramsf = 2
        super().__init__()
        self.line = "start"

    def generateRandomQuestion(self):
        time = now()
        self.timestamp = str(time)
        seed(time)
        self.generateRandomParams()

    # must override
    def generateRandomParams(self):
        self.a = sffloat(randint(2,8), self.paramsf)
        self.b = sffloat(randint(2,8), self.paramsf)
        self.c = sffloat(randint(2,8), self.paramsf)
    
    # must override
    @property
    def correctAnswer(self):
        return sqrt(self.a**2 + self.b**2 + self.c**2)
    
    def getHash(self):
        inputstr = self.ID + self.email + self.timestamp + str(self.correctAnswer)
        m = hashlib.md5(inputstr.encode('utf-8'))
        return m.hexdigest()        
    
    @property
    def successCode(self):
        return "{0}:{1}:{2}:{3}".format(
            self.ID, 
            self.email, 
            self.timestamp, 
            self.getHash()
            )
        
    def verifySuccess(self, code):
        seed(int(self.timestamp))
        self.generateRandomParams(code[2])
        self.email = code[1]
        if code[0] == self.ID and code[3] == self.getHash():
            return "VERIFIED"
        else:
            return "NOT VERIFIED"
        
    def showQuestion(self):
        print(self.question.format(self.a, self.b, self.c))
        
    def getUserEmail(self):
        self.email = input("Enter your email name (without @hanovernorwichschools.org): ")
        
    def getUserAnswer(self):
        try:
            self.rawanswer = input("Enter your answer: ")
            self.answer = float(self.rawanswer)
        except (ValueError, LookupError):
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
            checkval = self.email.split(':')
            if len(checkval) == 4:
                print(self.verifySuccess(checkval))
                self.line = "finish"
            else:
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
            print("Your success code is {0}".format(self.successCode))
            self.line = "finished"
        elif self.line == "incorrect":
            print("I'm sorry. You answered {0}.".format(self.answer))
            print("The correct answer is {0}.".format(self.correctAnswer))
            print("Try again!")
            self.line = "askquestion"
        elif self.line == "quit":
            print("See you later!")
            self.line = "finished"
            

if __name__ == "__main__":
    myapp = VectorMagnitudeExample()
    myapp.run()
    #myapp.userInteract()
    # VM01:eric.dennison:1566665625116:27ba14ec89ba5bbf838c3d16230a3039
    # VM01:eric.dennison:1566666259794:5c7940b9fdad4a516cb473357c33f1ea
    