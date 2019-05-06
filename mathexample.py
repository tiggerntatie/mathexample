# mathexample
from browser import open
from random import randint
from math import sqrt


class VectorMagnitudeExample:
    
    question = "Compute the magnitude of the vector, <{0},{1},{2}>:"
    
    def __init__(self):
        self.a = randint(2,8)
        self.b = randint(2,8)
        self.c = randint(2,8)
    
    @property
    def correctAnswer(self):
        return sqrt(self.a**2 + self.b**2 + self.c**2)
        
    
    