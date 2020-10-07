#%%
import random
import math
import sympy

def isPrime(number, trials=300):
    '''
    Prime number checker using Miller-Rabin Primality Test
    Arguments:
    number: The number to be checked
    trials: Totals of trials to check and potentially confirm whether a number is prime or not
    '''
    if number < 2 or number % 2 == 0 or number % 3 ==0:
        return False
    if number == 2 or number == 3:
        return True
    for i in range(2,11):
        if number % i == 0:
            return False 
    
    r = 0
    s = number - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(trials):
        a = random.randrange(2, number - 1)
        x = pow(a, s, number)
        if x == 1 or x == number - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, number)
            if x == number - 1:
                break
            else:
                return False
    return True

def getPrime(bit_size):
    if bit_size <= 1:
        return None
    if bit_size == 2:
        return random.randrange(2,4)
    rand_start = 2 ** (bit_size-1)
    rand_end = 2 ** bit_size
    while True:
         n = random.randrange(rand_start,rand_end)
         if isPrime(n,300):
             return n
     
def primRoots(modulo,size = 1):
    primRoots = []
    coprimes = {n for n in range(1, modulo) if math.gcd(n, modulo) == 1}
    for g in range(1,modulo):
        powers = set()
        for power in range(1,modulo):
            powers.add(pow(g, power, modulo))
            if coprimes == powers:
                primRoots.append(g)
                if len(primRoots) == size:
                    return primRoots
    return primRoots
    #return [g for g in range(1, modulo) if coprimes == {pow(g, powers, modulo) for powers in range(1, modulo)}]

 



# %%
# for i in range(13):
#     a = getPrime(i+1)    
#     if a:
#         print(a)
#         print(primRoots(a,1))
# %%
