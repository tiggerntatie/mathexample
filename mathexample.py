# mathexample
import sys
import hashlib
import base64
from abc import ABC, abstractmethod
from collections import namedtuple

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

# lfunc is the prompt for the level,
# cfunc returns correct value for this level
# nextscore is the score received for success
Level = namedtuple('Level', 'lprompt input test cfunc nextscore')

class Question:
    
    def __init__(self, prompt, inputfunc, testfunc):
        self._prompt = prompt
        self._inputfunc = inputfunc
        self._testfunc = testfunc
        
    def prompt(self):
        self._prompt()
        
    def getinput(self):
        self._inputfunc()
        
    def iscorrect(self, answer):
        return self._testfunc(answer)

class MathExample(App, ABC):

    def __init__(self):
        super().__init__()
        self.score = -1
        self._state = "prompt"
        
    def step(self):
        if self.score == -1:
            self.getUserEmail()
            if self.verifySuccess():
                self.score = -2
            else:
                self.generateRandomQuestion()
                self.score = 0
        elif self.score >= 0:
            if self.levels[self.score].lprompt:
                if self._state == "prompt":
                    self.levels[self.score].lprompt()
                    self._state = "input"
                elif self._state == "input":
                    self.answer = self.levels[self.score].input()
                    self._state = "eval"
                elif self._state == "eval":
                    self._state = "prompt"
                    success = self.levels[self.score].test(self.answer)
                    if success:
                        self.score = self.levels[self.score].nextscore
                    else:
                        correct = self.levels[self.levels[self.score].nextscore].cfunc()
                        print("I'm sorry. You answered {0}".format(self.answer))
                        print("The correct answer is {0}".format(correct))
                        print("Your partial success code is: {0}".format(self.successCode))
                        print("Try again :)")
                        self.score = -2
            else:
                print("Congratulations! Your success code is: {0}".format(self.successCode))
                self.score = -2

    def generateRandomQuestion(self):
        time = now() % 10000
        self.timestamp = str(time)
        seed(time)
        self.generateRandomParams()
    
    @abstractmethod
    def generateRandomParams(self):
        pass

    def getFloatAnswer(self):
        self.rawanswer = None
        try:
            self.rawanswer = float(input("Enter your answer: "))
        except (ValueError, LookupError):
            pass
        return self.rawanswer

    def getHash(self):
        inputstr = self.ID + self.email + str(self.score) + self.timestamp + str(self.levels[self.score].cfunc())
        m = hashlib.sha256(inputstr.encode('utf-8'))
        return m.hexdigest()[:9]        

    def getUserEmail(self):
        print("Enter your email name")
        self.email = input("(without @hanovernorwichschools.org): ")
        
    @property
    def successCode(self):
        return "{0}:{1}:{2}:{3}:{4}".format(
            self.ID, 
            self.email, 
            self.score,
            self.timestamp, 
            self.getHash()
            )
        
    def isSuccessCode(self, code):
        checkval = code.split(':')
        if len(checkval) == 5:
            return checkval
        else:
            return False
            
    def verifySuccess(self):
        code = self.isSuccessCode(self.email)
        if code:
            self.timestamp = code[3]
            seed(int(code[3]))
            self.generateRandomParams()
            self.score = int(code[2])
            self.email = code[1]
            if code[0] == self.ID and code[4] == self.getHash():
                print("VERIFIED: {0} points awarded to {1}".format(self.score, self.email))
            else:
                print("NOT VERIFIED")
            return True
        else:
            return False




if __name__ == "__main__":

    class VectorMagnitudeExample(MathExample):
        
        ID = "VM01"
        
        def __init__(self):
            super().__init__()
            self.levels = {
                0: Level(
                    self.promptA2, 
                    self.getFloatAnswer, 
                    lambda answer: self.correctA2().equivalent_to_float(answer),
                    lambda: 0, 
                    2),
                2: Level(
                    lambda: print("Good! And what is the square of the second component?"),
                    self.getFloatAnswer,
                    lambda answer: self.correctB2().equivalent_to_float(answer),
                    self.correctA2,
                    4),
                4: Level(
                    lambda: print("Yes :) And the square of the third component?"),
                    self.getFloatAnswer,
                    lambda answer: self.correctC2().equivalent_to_float(answer),
                    self.correctB2,
                    6),
                6: Level(
                    lambda: print("Awesome! Next, what is the sum of the squares?"),
                    self.getFloatAnswer,
                    lambda answer: self.correctSum().equivalent_to_float(answer),
                    self.correctC2,
                    8),
                8: Level(
                    lambda: print("Just one more! What is the magnitude of the vector <{0},{1},{2}>?".format(self.a, self.b, self.c)),
                    self.getFloatAnswer,
                    lambda answer: self.correctMag().equivalent_to_float(answer),
                    self.correctSum,
                    10),
                10: Level(None, None, None, self.correctMag, None),
            }
    
        def generateRandomParams(self):
            self.a = sffloat(randint(2,8), 2)
            self.b = sffloat(randint(2,8), 2)
            self.c = sffloat(randint(2,8), 2)
        
        def correctA2(self):
            return self.a**2
            
        def correctB2(self):
            return self.b**2
            
        def correctC2(self):
            return self.c**2
    
        def correctSum(self):
            return self.a**2 + self.b**2 + self.c**2
            
        def correctMag(self):
            return sqrt(self.a**2 + self.b**2 + self.c**2)
    
        def promptA2(self):
            print("Compute the magnitude of this vector: <{0},{1},{2}>.".format(self.a, self.b, self.c))
            print("First, what is the square of the first component?")



    myapp = VectorMagnitudeExample()
    myapp.run()

    # VM01:eric.dennison:10:1566675826951:ad89ac21cd13ab44e779200be46c6ec4
    