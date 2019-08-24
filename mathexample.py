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
Level = namedtuple('Level', 'lfunc cfunc nextscore')

class MathExample(App, ABC):

    def __init__(self):
        super().__init__()
        self.score = -1
        
    def step(self):
        if self.score == -1:
            self.getUserEmail()
            if self.verifySuccess():
                self.score = -2
            else:
                self.generateRandomQuestion()
                self.score = 0
        elif self.score >= 0:
            if self.levels[self.score].lfunc:
                success, answer, correct = self.levels[self.score].lfunc()
                if success:
                    self.score = self.levels[self.score].nextscore
                else:
                    print("I'm sorry. You answered {0}".format(answer))
                    print("The correct answer is {0}".format(correct))
                    print("Your partial success code is: {0}".format(self.successCode))
                    self.score = -2
            else:
                print("Congratulations! Your success code is: {0}".format(self.successCode))
                self.score = -2

    def generateRandomQuestion(self):
        time = now()
        self.timestamp = str(time)
        seed(time)
        self.generateRandomParams()
    
    @abstractmethod
    def generateRandomParams(self):
        pass

    def getFloatAnswer(self):
        try:
            self.rawanswer = input("Enter your answer: ")
            self.answer = float(self.rawanswer)
        except (ValueError, LookupError):
            self.answer = None

    def getHash(self):
        print(self.levels)
        inputstr = self.ID + self.email + str(self.score) + self.timestamp + str(self.levels[self.score].cfunc())
        m = hashlib.md5(inputstr.encode('utf-8'))
        return m.hexdigest()        

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
            self.score = code[2]
            self.email = code[1]
            if code[0] == self.ID and code[4] == self.getHash():
                print("VERIFIED")
            else:
                print("NOT VERIFIED")
            return True
        else:
            return False

class VectorMagnitudeExample(MathExample):
    
    ID = "VM01"
    
    def __init__(self):
        super().__init__()
        self.levels = {
            0: Level(self.questA2, None, 2),
            2: Level(self.questB2, self.correctA2, 4),
            4: Level(self.questC2, self.correctB2, 6),
            6: Level(self.questSum, self.correctC2, 8),
            8: Level(self.questMag, self.correctSum, 10),
            10: Level(None, self.correctMag, None),
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

    def questA2(self):
        print("Compute the magnitude of this vector: <{0},{1},{2}>.".format(self.a, self.b, self.c))
        print("First, what is the square of the first component?")
        self.getFloatAnswer()
        return self.correctA2().equivalent_to_float(self.answer), self.answer, self.correctA2()

    def questB2(self):
        print("And what is the square of the second component?")
        self.getFloatAnswer()
        return self.correctB2().equivalent_to_float(self.answer), self.answer, self.correctB2()

    def questC2(self):
        print("And the square of the third component?")
        self.getFloatAnswer()
        return self.correctC2().equivalent_to_float(self.answer), self.answer, self.correctC2()

    def questSum(self):
        print("Next, what is the sum of the squares?")
        self.getFloatAnswer()
        return self.correctSum().equivalent_to_float(self.answer), self.answer, self.correctSum()

    def questMag(self):
        print("Finally, what is the magnitude of the vector <{0},{1},{2}>?".format(self.a, self.b, self.c))
        self.getFloatAnswer()
        return self.correctMag().equivalent_to_float(self.answer), self.answer, self.correctMag()


if __name__ == "__main__":
    myapp = VectorMagnitudeExample()
    myapp.run()
    #myapp.userInteract()
    # VM01:eric.dennison:1566665625116:27ba14ec89ba5bbf838c3d16230a3039
    # VM01:eric.dennison:1566666259794:5c7940b9fdad4a516cb473357c33f1ea
    