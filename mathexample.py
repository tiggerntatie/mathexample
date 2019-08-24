# mathexample
import sys
import hashlib
import base64
from abc import ABC, abstractmethod

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


class MathExample(App, ABC):

    def __init__(self, firststate):
        super().__init__()
        self.line = "_"
        self._firststate = firststate
        
    def step(self):
        if self.line == "_":
            self.getUserEmail()
            if self.verifySuccess():
                self.line = "__"
            else:
                self.line = self._firststate
        else:
            self.main()
        
    def generateRandomQuestion(self):
        time = now()
        self.timestamp = str(time)
        seed(time)
        self.generateRandomParams()
    
    @abstractmethod
    def main(self):
        pass
    
    @abstractmethod
    def generateRandomParams(self):
        pass

    @abstractmethod
    @property
    def correctAnswer(self):
        pass

    def getHash(self):
        inputstr = self.ID + self.email + self.timestamp + str(self.correctAnswer)
        m = hashlib.md5(inputstr.encode('utf-8'))
        return m.hexdigest()        

    def getUserEmail(self):
        self.email = input("Enter your email name (without @hanovernorwichschools.org): ")
        
    @property
    def successCode(self):
        return "{0}:{1}:{2}:{3}".format(
            self.ID, 
            self.email, 
            self.timestamp, 
            self.getHash()
            )
        
    def isSuccessCode(self, code):
        checkval = code.split(':')
        if len(checkval) == 4:
            return checkval
        else:
            return False
            
    def verifySuccess(self):
        code = self.isSuccessCode(self.email)
        if code:
            seed(int(code[2]))
            self.generateRandomParams()
            self.email = code[1]
            if code[0] == self.ID and code[3] == self.getHash():
                print("VERIFIED")
            else:
                print("NOT VERIFIED")
            return True
        else:
            return False

class VectorMagnitudeExample(MathExample):
    
    question = "Compute the magnitude of this vector: <{0},{1},{2}>."
    ID = "VM01"
    
    def __init__(self):
        super().__init__("askquestion")

    def generateRandomParams(self):
        self.a = sffloat(randint(2,8), 2)
        self.b = sffloat(randint(2,8), 2)
        self.c = sffloat(randint(2,8), 2)
    
    @property
    def correctAnswer(self):
        return sqrt(self.a**2 + self.b**2 + self.c**2)
    
    def showQuestion(self):
        print(self.question.format(self.a, self.b, self.c))
        
    def getUserAnswer(self):
        try:
            self.rawanswer = input("Enter your answer: ")
            self.answer = float(self.rawanswer)
        except (ValueError, LookupError):
            self.answer = None
        
    def showAnswer(self):
        print("Your answer is: ", self.answer)
        print("The correct answer is: ", self.correctAnswer)
        
    def main(self):
        if self.line == "askquestion":
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
    