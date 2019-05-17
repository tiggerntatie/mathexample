# mathexample
import sys
sffloatpath = "https://tiggerntatie.github.io/sffloat/"
if sffloatpath not in sys.path:
    sys.path.append(sffloatpath)

from sffloat import sffloat
from browser import window
from random import randint
from math import sqrt
from ggame import App


class VectorMagnitudeExample:
    
    question = "Compute the magnitude of this vector: <{0},{1},{2}>."
    
    def __init__(self):
        self.answer = None
        self.paramsf = 2
        self.generateRandomQuestion()

    def generateRandomQuestion(self):
        self.a = sffloat(randint(2,8), self.paramsf)
        self.b = sffloat(randint(2,8), self.paramsf)
        self.c = sffloat(randint(2,8), self.paramsf)
        
    
    @property
    def correctAnswer(self):
        return sqrt(self.a**2 + self.b**2 + self.c**2)
        
    def showQuestion(self):
        print(self.question.format(self.a, self.b, self.c))
        
    def getUserAnswer(self):
        self.answer = sffloat(float(input("Enter your answer: ")))
        
    def userInteract(self):
        while not self.answer or not self.correctAnswer.equivalent_to_float(self.answer):
            self.showQuestion()
            self.getUserAnswer()
            self.generateRandomQuestion()
        

if __name__ == "__main__":
    myapp = App()
    myapp.run()
    ex = VectorMagnitudeExample()
    ex.userInteract()
    
    