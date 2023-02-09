import numpy as np
import random

# class of probability distribution
class Cl_distribution:
    def __init__(self, degree_sequence):
        self.mydegree_sequence = degree_sequence

    # density funciton pi(i) = Di/2m
    def pdf(self, i):
        return self.mydegree_sequence[i]/np.sum(self.mydegree_sequence)

    # cumulative density funciton
    def cdf(self):
        length = len(self.mydegree_sequence)
        p = [0]*length
        p[0] = self.pdf(0)
        for  i in range (1,length):
            p[i] = p[i-1] + self.pdf(i)
        return p

    # random value generator
    def rvs(self):
        u = random.uniform(0,1)
        p = self.cdf()
        for i in range(len(self.mydegree_sequence)):
            if u <= p[i]:
                return i
        
if __name__ == '__main__': 
    degree_sequence = [1,1,2,2,4,4,4]
    cl_helper = Cl_distribution(degree_sequence)
    pdf0 = cl_helper.pdf(0)
    print(pdf0)
    cdf = cl_helper.cdf()
    print(cdf)
    i = cl_helper.rvs()
    print(i)

    
