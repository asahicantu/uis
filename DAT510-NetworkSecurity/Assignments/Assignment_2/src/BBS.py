#%%
import sys
import random
import sympy
class BBS(object):
    def __init__(self, bits):
        self.n = self.generateN(bits)
        bit_size = len(bin(bits))
        seed = random.getrandbits(bit_size)
        self.state = None
        self.setSeed(seed)  

    def setSeed(self, seed):
        self.state = seed % self.n

    def generateN(self, bits):
        half_bits = bits // 2
        rangeStart = 2 ** (half_bits -1)
        rangeEnd = 2 ** half_bits 
        p = sympy.randprime(rangeStart,rangeEnd)
        q = sympy.randprime(rangeStart,rangeEnd)
        if p != q:
            return p * q
        else: # Recalculate in case p == q
            return self.generateN(bits)

    

    def next(self, numBits):
        '''Returns up to numBit random bits'''
        result = 0
        for _ in range(numBits):
            self.state = (self.state**2) % self.n
            result = (result << 1) | (self.state & 1)
        return result    

# %%
