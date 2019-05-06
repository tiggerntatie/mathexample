# mathexample
from browser import window
from random import randint
from math import sqrt


class VectorMagnitudeExample:
    
    question = "Compute the magnitude of this vector: <{0},{1},{2}>."
    
    def __init__(self):
        self.answer = None
        self.generateRandomQuestion()
    
    def generateRandomQuestion(self):
        self.a = randint(2,8)
        self.b = randint(2,8)
        self.c = randint(2,8)
        
    
    @property
    def correctAnswer(self):
        return sqrt(self.a**2 + self.b**2 + self.c**2)
        
    def showQuestion(self):
        print(self.question.format(self.a, self.b, self.c))
        
    def getUserAnswer(self):
        self.answer = float(input("Enter your answer: "))
        
    def userInteract(self):
        while not self.answer or self.answer != self.correctAnswer:
            self.showQuestion()
            self.getUserAnswer()
            self.generateRandomQuestion()
        
        

if __name__ == "__main__":
    ex = VectorMagnitudeExample()
    ex.userInteract()
    
    