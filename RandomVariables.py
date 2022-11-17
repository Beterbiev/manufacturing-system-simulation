import math

class RandomVariables:
	
    def __init__(self, sample):
        self.sample = sample

    def exp(self, mean):
        x = [-mean * math.log(u) for u in self.sample]

        return x
