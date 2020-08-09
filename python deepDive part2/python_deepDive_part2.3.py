# python_deepDive part 2, Module 3
# python version: 3.7.3

"""
This module contains the following: 
    1. Generators: a type of iterators.
        a. Genertor Factories
        b. Generator comprehensions
        c. Genertor function: A function which uses a yield statement is called as a generator function
        d. Generator expressions and Performance


Definitions:  
    yield keyword:
        1. it emits a vlaue 
        2. function is effectively suspended but it retains it's current state
        3. calling next on the function resumes running the fucntion right after the yield statement 
        4. If the function returns instead of yielding(finish running) -->  StopIteration 
"""

#Yielding and Generators
def my_func():
    yield "yield statement 1"
    yield "yield statement 2"

f = my_func()
type(f) # returns < generator object >

"__next__" in dir(f)  #returns True
"__iter__" in dir(f)  #returns True
iter(f) is f          #returns True

f.__next__() # returns "yield statement 1"
next(f)      # returns "yield statement 2"

#let's take another example;
def silly():
    yield "the"
    yield "misnistry"
    yield "of"
    yield "silly"
    if True:
        return "Sorry, all done" 
    yield "walks"

gen = silly()

[next(gen) for _ in range(4)]
# print(next(gen))   # we will get a  "StopIteration: Sorry, all done" error message
# if we call next(gen) again, we will get a "StopIteration" error. 

#Application: 
#let's try to create a Factorial Iterator by implementing the iterator protocol
#Method 1
import math 

class FactIter:
    def __init__(self, n):
        self.n = n 
        self.i = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        else:
            result = math.factorial(self.i)
            self.i+=1 
            return result

fact_iter= FactIter(5)        
result = list(fact_iter)  #return [1, 1, 2, 6, 24]

#Method 2 : Implementing the above using a closure 
def fact():
    i = 0 

    def inner():
        nonlocal i
        value = math.factorial(i)
        i +=1
        return value 
    return inner

f = fact()
result = [f() for _ in range(5)]  #returns [1, 1, 2, 6, 24]

# this currently has no upper limit,so we can use the iter() function to set the sentinal value
f = fact()
fact_iter = iter(f, math.factorial(10))

result = [value for value in fact_iter]  #return [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]

#Method 3: Implementing the above using a Generators. 
def fact(n):
    for i in range(n):
        yield math.factorial(i)

gen = fact(7)

next(gen)  #return 1
next(gen)  #return 1
next(gen)  #return 2
next(gen)  #return 6
next(gen)  #return 4

#Similarly we can create a Generator to return squared values 
def square(n):
    for i in range(n):
        yield i**2

sq = square(5)
result = [value for value in sq]  #return [0, 1, 4, 9, 16]

#Application: Creating a Fibonacci Sequence 

#MEthod 1: recursion : Highly inefficient 
from functools import lru_cache 

@lru_cache(2**8)
def fib_recursive(n):
    return 1 if n<2 else fib_recursive(n-1) + fib_recursive(n-2)

result = [fib_recursive(i) for i in range(7)]  # return [1, 1, 2, 3, 5, 8, 13]

#Method 2 : using a loop
def fib_standard(n):
    fib_0 = 1
    fib_1 = 1
    for i in range(n-1):
        fib_0, fib_1 = fib_1, fib_0 + fib_1
    return fib_1

result = [fib_standard(i) for i in range(7)]  #return [1, 1, 2, 3, 5, 8, 13]

# Creating a iterator for lazy evaluation 
class FibIter:
    def __init__(self, n):
        self.n = n 
        self.i = 0 

    def __iter__(self):
        return self 
    
    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        else:
            value = fib_standard(self.i)
            self.i +=1 
            return value

fib_iter = FibIter(6)
result = [num for num in fib_iter]  #return [1, 1, 2, 3, 5, 8]

#Instead we can just create a generator
def fib_generator(n):
    fib_0 = 1
    yield fib_0
    fib_1 = 1
    yield fib_1
    for i in range(n-2):
        fib_0, fib_1 = fib_1, fib_0 + fib_1
        yield fib_1

gen = fib_generator(9)
result = [value for value in gen]  #returns [1, 1, 2, 3, 5, 8, 13, 21, 34]

#Checking timing efficiency
from timeit import timeit

# result = timeit("list(FibIter(5000))", globals = globals(), number = 1)  # return 2.110589199999999
# result = timeit("list(fib_generator(5000))", globals = globals(), number = 1)  # return 0.0014628999999999337

#we can see that generators are highly efficient

"""Avoiding creation of iterator for an iterable everytime we want to loop through it"""
def square_gen(n):
    for i in range(n):
        yield i**2

class Square:
    def __init__(self, n):
        self.n = n 

    def __iter__(self):
        return square_gen(self.n)

sq = Square(6)

#Now we can iterate it as many time as we want.
result = [value for value in sq] #return [0, 1, 4, 9, 16, 25]
result = list(sq) # return [0, 1, 4, 9, 16, 25]

#cleaning the code a bit 
class Square:
    def __init__(self, n):
        self.n = n 

    def __iter__(self):
        return Square.square_gen(self.n)
    
    @staticmethod
    def square_gen(n):
        for i in range(n):
            yield i**2

sq = Square(6)
result = [value for value in sq] #return [0, 1, 4, 9, 16, 25]
result = list(sq) #return [0, 1, 4, 9, 16, 25]

#example: Card Deck
from collections import namedtuple

Card = namedtuple("Card", "rank suit")
SUITS = ["SPADES", "HEARTS", "DIAMONDS", "CLUBS"]
RANKS = tuple(range(2,11)) + tuple("JQKA")

#Method 1
def card_generator():
    for i in range(len(SUITS)* len(RANKS)):
        suit = SUITS[i // len(RANKS)]
        rank = RANKS[i % len(RANKS)]
        card = Card(rank, suit)
        yield card

result = [card for card in card_generator()]

#Method 2
def card_generator():
    for suit in SUITS:
        for rank in RANKS:
            yield Card(rank, suit )

result = [card for card in card_generator()]

#let's convert it into a iterable:
class CardDeck:

    SUITS = ["SPADES", "HEARTS", "DIAMONDS", "CLUBS"]
    RANKS = tuple(range(2,11)) + tuple("JQKA")
    Card = namedtuple("Card", "rank suit")

    def __iter__(self):
        return CardDeck.card_gen()

    @staticmethod
    def card_gen():
        for suit in CardDeck.SUITS:
            for rank in CardDeck.RANKS:
                yield Card(rank, suit )

deck = CardDeck()
result = [card for card in deck]
result = list(deck)

#adding the __reverse__ card property.
class CardDeck:

    SUITS = ["SPADES", "HEARTS", "DIAMONDS", "CLUBS"]
    RANKS = tuple(range(2,11)) + tuple("JQKA")
    Card = namedtuple("Card", "rank suit")

    def __iter__(self):
        return CardDeck.card_gen()
    
    def __reversed__(self):
        return CardDeck.reversed_card_gen()

    @staticmethod
    def card_gen():
        for suit in CardDeck.SUITS:
            for rank in CardDeck.RANKS:
                yield Card(rank, suit)

    @staticmethod
    def reversed_card_gen():
        for suit in reversed(CardDeck.SUITS): # since this is a tuple we can use it's built in reverse method
            for rank in reversed(CardDeck.RANKS):
                yield Card(rank, suit )

deck = CardDeck()
rev_decl = reversed(deck)

""" Generator expressions and Performance
--> A genertor has all the properties which a list comprehension has.
--> Generator expresssions are memory efficent, as they don't have to load everything in the memory at once but instead do the calculations as per the request. 
--> if you have to loop through the entire data the timings are also same. 
"""
list_comprehension = [i**2 for i in range(5)]  
#This is a eager execution, i.e the objects gets created at the time of creation 

generator_expression = (i**2 for i in range(5))  
#This is a lazy evaluation, i.e objects inside are not created until asked.

#let's dissemble it to see if there is a difference in the way python creates them. 
import dis 
exp = compile('[i**2 for i in range(5)]', filename = "<string>", mode = "eval")
# dis.dis(exp)

#Performace Characterstics 1: Timing
import math
def binomial_coefficent(n, k): 
    return math.factorial(n) /(math.factorial(k) * math.factorial(n-k))

def pascal_list(size):
    l = [[binomial_coefficent(n,k) for k in range(n+1)] for n in range(size+1)]
    for row in l:
        for item in row:
            pass 

def pascal_gen(size):
    g = ((binomial_coefficent(n,k) for k in range(n+1)) for n in range(size+1))
    for row in g:
        for item in row:
            pass 

#timing it
"""
size = 600
result = timeit("pascal_list(size)", globals = globals(), number = 1) # returns  4.7214986
result = timeit("pascal_gen(size)", globals = globals(), number = 1) # returns  4.763830899999999
"""

#Performace Characterstics 2: Memeory consumption
import tracemalloc  # can used to check the max amount of memory consumed during a process


def pascal_list(size):
    l = [[binomial_coefficent(n,k) for k in range(n+1)] for n in range(size+1)]
    for row in l:
        for item in row:
            pass 
    stats = tracemalloc.take_snapshot().statistics("lineno")
    return stats[0].size, "bytes"

def pascal_gen(size):
    g = ((binomial_coefficent(n,k) for k in range(n+1)) for n in range(size+1))
    for row in g:
        for item in row:
            pass 
    stats = tracemalloc.take_snapshot().statistics("lineno")
    return stats[0].size, "bytes"


tracemalloc.start()
result = pascal_list(300)  #return 1090728 bytes

tracemalloc.stop()
tracemalloc.clear_traces()
tracemalloc.start()

result = pascal_gen(300)   # returns 1136 bytes
print(result)