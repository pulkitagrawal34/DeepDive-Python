# python_deepDive part 2 , Module 2
# python version: 3.7.3

"""
This module contains the following:
    Iterable : It is a container type of object and we can list out the elements one by one. But the order in which they come is not guranteed.
        for example: sets are iterable but their order is not guranteed.
        a. creating a iterator: An iterator is an object that implements:  
                                1. __iter__
                                2. __next__
            These are called as Iterator protocols.
        But in case, we have not implemented the iterator protocol and instead definied __getitem__ method, that would also work. 
        b. Cyclic Iterators
        c. Lazy evaluation 
        d. Iterating Callables
        e. delegating Iterators
"""
#Example 1 
class Square:

    def __init__(self, length):
        self.i = 0 
        self.length = length

    def __len__(self):
        return self.length

    def __next__(self):
        if self.i >= self.length:
            raise StopIteration
        else:
            result = self.i**2
            self.i+=1
            return result 

sq = Square(5)

next(sq) #returns 0
next(sq) #returns 1
next(sq) #returns 4
next(sq) #returns 9
next(sq) #returns 16

#we can also iterate through this using a While loop
while True:
    try: 
        next(sq)
    except StopIteration:
        break

#returns 0,1,4,9,16
#but still we cannot run a for loop to extract the numbers in this collection

#Example 2
import random

class RandomNumbers:

    def __init__(self, length, *, range_min = 0, range_max = 10):

        self.length = length 
        self.range_min = range_min
        self.range_max = range_max
        self.num_requested = 0 
    
    def __len__(self):
        return self.length
    
    def __next__(self):
        if self.num_requested >= self.length:
            raise StopIteration
        else:
            self.num_requested +=1
            return random.randint(self.range_min, self.range_max)

numbers = RandomNumbers(3)

next(numbers) # returns 3
next(numbers) # returns 2
next(numbers) # returns 1

#but if we try to call next(numbers) now, it will raise a StopIteration error

#making Example 1 a iterator 
class Square:

    def __init__(self, length):
        self.length = length
        self.i = 0 

    def __len__(self):
        return self.length

    def __next__(self):
        # print("__next__ called")
        if self.i >= self.length:
            raise StopIteration
        else:
            result = self.i**2
            self.i+=1
            return result 

    def __iter__(self): #This is a special method to tell python that it's an iterable  
        # print("__iter__ called")
        return self

sq = Square(10)
#now we can run a for loop, implement a list comprehension etc...
[item for item in sq] #returns [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

#we can use enumerate as well.
sq = Square(5)
result = list(enumerate(sq)) #returns [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]

#using sorted 
sq = Square(7)
result = sorted(sq, reverse = True) # return [36, 25, 16, 9, 4, 1, 0]

#How does python does it??

#let's again this example: 

sq = Square(5)

for item in sq:
    item # replace it with print(item) to see the results

#Python returns this:
"""
__iter__ called
__next__ called
0
__next__ called
1
__next__ called
4
__next__ called
9
__next__ called
16
__next__ called
"""

#So we can see python first calls the __iter__ method and then the __next__ method is called. 
#So what actually python does is the following:
sq = Square(5)
#python is then calling the iter() function, which inherently calles the __iter__ method 
sq_iterator = iter(sq)

while True:
    try:
        next(sq_iterator) # replace it with print(next(sq_iterator)) to see the outputs and uncomment print statements from the class to see the below shown result. 
    except StopIteration:
        break 

#But we still can't restart the iterator once we have exhausted it. 

"""
Solution:
Maintaining the data collection should be one object.
Iterating over the data should be a saperate object.-- >Iterator

i.e The collection is iterable but the iterator is responsible for iterating over the data

The iterable is created once.
The iterator is created every time we want to start a fresh iteration. 
"""
class Cities:
    def __init__(self):
        self._cities = ["Paris", "Berlin", "Rome", "Madrid", "London"]
        self._index = 0

    def __len__(self):
        return len(self._cities)

class CityIterator:
    def __init__(self, city_obj):
        self._city_obj = city_obj
        self._index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._city_obj):
            raise StopIteration
        else:
            item = self._city_obj._cities[self._index]
            self._index +=1
            return item

cities = Cities()
city_iterable = CityIterator(cities)

result = [item.upper() for item in city_iterable] # ['PARIS', 'BERLIN', 'ROME', 'MADRID', 'LONDON']
"""
Once we run it, city_iterable has been exhausted.
But we can always recreate the iterator and use it, but now we don't neeed to create the Cities Object.(Helpful in cases when cities object contains a huge amount of data )
But still the problem is we need to remember the Iterator class to pass the city object and iterate through it. 
"""

#Solution: create a __iter__ method within the Iterable, and just return a new instance of the iterator

class CityIterator:
    def __init__(self, city_obj):
        self._city_obj = city_obj
        self._index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._city_obj):
            raise StopIteration
        else:
            item = self._city_obj._cities[self._index]
            self._index +=1
            return item

class Cities:
    def __init__(self):
        self._cities = ["Paris", "Berlin", "Rome", "Madrid", "London"]
        self._index = 0

    def __len__(self):
        return len(self._cities)

    def __iter__(self):
        return CityIterator(self)

cities = Cities()
result = [item.upper() for item in cities] 

#A more cleaned-up way of writing this code will be:
class Cities:
    def __init__(self):
        self._cities = ["Paris", "Berlin", "Rome", "Madrid", "London"]
        self._index = 0

    def __len__(self):
        return len(self._cities)

    def __iter__(self):
        return self.CityIterator(self)

    class CityIterator:

        def __init__(self, city_obj):
            self._city_obj = city_obj
            self._index = 0

        def __iter__(self):
            return self
        
        def __next__(self):
            if self._index >= len(self._city_obj):
                raise StopIteration
            else:
                item = self._city_obj._cities[self._index]
                self._index +=1
                return item

cities = Cities()
result = [item.upper() for item in cities] #returns ['PARIS', 'BERLIN', 'ROME', 'MADRID', 'LONDON']
result = list(enumerate(cities)) #returns [(0, 'Paris'), (1, 'Berlin'), (2, 'Rome'), (3, 'Madrid'), (4, 'London')]

#adding sequence type properties to this class  
class Cities:
    def __init__(self):
        self._cities = ["Paris", "Berlin", "Rome", "Madrid", "London"]
        self._index = 0

    def __len__(self):
        return len(self._cities)

    def __iter__(self):
        return self.CityIterator(self)

    def __getitem__(self, s):
        return self._cities[s]

    class CityIterator:

        def __init__(self, city_obj):
            self._city_obj = city_obj
            self._index = 0

        def __iter__(self):
            return self
        
        def __next__(self):
            if self._index >= len(self._city_obj):
                raise StopIteration
            else:
                item = self._city_obj._cities[self._index]
                self._index +=1
                return item

cities = Cities()

result = cities[1]  #return "Berlin"
result = cities[:3] #return ['Paris', 'Berlin', 'Rome']

#Application of Iterators Example 1:
#Cyclic Iterators 

class CyclicIterators:

    def __init__(self, lst):
        self.lst = lst 
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        result = self.lst[self.i % len(self.lst)] # this allows us to keep looping infinitely
        self.i += 1
        return result 

#let's say we want to get something like this 1N, 2S, 3E, 4W, 5N, 6S, 7E, 8W, 9N.....
n = 10 
iter_cycle = CyclicIterators("NSEW")

#Method 1
result = [f'{i}{next(iter_cycle)}' for i in range(1, n+1)] # return ['1N', '2S', '3E', '4W', '5N', '6S', '7E', '8W', '9N', '10S']

#Method 2: Using Zip
n = 10 
iter_cycle = CyclicIterators("NSEW")

result =  [f'{index}{direction}' for index, direction in zip(range(1, n+1), iter_cycle)] #return ['1N', '2S', '3E', '4W', '5N', '6S', '7E', '8W', '9N', '10S']

#Method 3: Using Zip and repeatition
n = 10 
result =  [str(number) + direction for number, direction in zip(range(1, n+1), "NSEW"*(n//4 +1))] #return ['1N', '2S', '3E', '4W', '5N', '6S', '7E', '8W', '9N', '10S']

#Method 4: Python has an built-in itertools module
import itertools 
n = 10 
iter_cycle = itertools.cycle("NSEW")

result = [str(i) + next(iter_cycle) for i in range(1, n+1)] #returns ['1N', '2S', '3E', '4W', '5N', '6S', '7E', '8W', '9N', '10S']

#trying to replicate built-in itertools.cycle for any iterable
class CyclicIterators:

    def __init__(self, iterable):
        self.iterable = iterable 
        self.iterator = iter(self.iterable)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            item = next(self.iterator)
        except StopIteration:
            self.iterator = iter(self.iterable)
            item = next(self.iterator)
        finally:
            return item

iter_cycle = CyclicIterators("abc")

result = [next(iter_cycle) for _ in range(10)]#returns ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a']

""" Lazy evaluation:
This is often used in class properties, where value of a property becomes known when the value is requested
 """

import math 
#Here we are trying to create area of the circle as a property which doesn't get created until it's called. 

class Circle:
    def __init__(self, r):
        self.radius = r
        self._area = None
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, r):
        self._radius = r
        self._area = None

    @property
    def area(self):
        if self._area is None:
            self._area = math.pi *(self.radius ** 2)
        return self._area

c = Circle(1)
result = c.radius
result = c.area #return 3.141592653589793

c.radius = 2
result = c.area #return 12.566370614359172

#we can do something similar with iterables, for example:
class Factorials:

    def __iter__(self):
        return self.FactIter()

    class FactIter:

        def __init__(self):
            self.i = 0 
        
        def __iter__(self):
            return self 
        
        def __next__(self):
            result = math.factorial(self.i)
            self.i+=1 
            return result


facts = Factorials()     #infinite iterable
facts_iter = iter(facts) #Here is the iterator, we cna do next(fact_iter) which we can do inifinitely many times.


#python iter() function 
#let's take the same example as we used before 

class Square:

    def __init__(self, n):
        self._n = n 
    
    def __len__(self):
        return self._n 
    
    def __getitem__(self, i):
        if i >= self._n :
            raise IndexError
        else:
            return i ** 2

sq = Square(5)
sq_iter = iter(sq)

"__iter__" in dir(sq_iter) #returns True
"__next__" in dir(sq_iter) #returns True

#even thoight we haven't defined these two methods, so how is python doing it using the __getitem__ method? 
#this is how it does it:

class SquaresIterator :
    def __init__(self, sq_obj):
        self._squares = sq_obj
        self._i = 0 

    def __iter__(self):
        return self 
    
    def __next__(self):
        if self._i >= len(self._squres):
            raise StopIteration
        else:
            result = self._squares[self.i]
            self._i +=1 
            return result

sq = Square(7)
sq_iterator = SquaresIterator(sq)

"__iter__" in dir(sq_iterator) #returns True
"__next__" in dir(sq_iterator) #returns True

#The SquareIterator defined above can be generalised for any sequence type:
class SequenceIterator :
    def __init__(self, sequence):
        self._sequence = sequence
        self._i = 0 

    def __iter__(self):
        return self 
    
    def __next__(self):
        if self._i >= len(self._sequence):
            raise StopIteration
        else:
            result = self._sequence[self.i]
            self._i +=1 
            return result


# print(result)

"""
Best to check if an object is iterable: Is by calling the iter() function on the object. 
"""
def is_iterable(obj):
    try:
        iter(obj)
        return True 
    except TypeError:
        return False


"""Iterating Callables"""

def counter():
    i = 0

    def func():
        nonlocal i 
        i+=1
        return i 
    return func 

cnt = counter()

cnt() #return 1 
cnt() #return 2


class CallableIterator:

    def __init__(self, callable, sentinal:"value at which it will stop iteration"):
        self.callable = callable 
        self.sentinal = sentinal
        
    def __iter__(self):
        return self

    def __next__(self):
        value = self.callable()
        if value == self.sentinal:
            raise StopIteration
        else:
            return value

cnt = counter()
cnt_iter = CallableIterator(cnt, 5)

result = [c for c in cnt_iter]  #return [1, 2, 3, 4]

#but there is a problem here, if we called next(c), it will return 6 
next(cnt_iter) # return 6 
#so we need to tell the iterator to stop returning the values once the StopIteration has been raised


class CallableIterator:

    def __init__(self, callable, sentinal):
        self.callable = callable 
        self.sentinal = sentinal
        self.is_consumed = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.is_consumed:
            raise StopIteration
            
        else:
            value = self.callable()

            if value == self.sentinal:
                self.is_consumed = True
                raise StopIteration
            else:
                return value

cnt = counter()
cnt_iter = CallableIterator(cnt, 5)

result = [c for c in cnt_iter]  #return [1, 2, 3, 4]
# next(cnt_iter) --> This will throw a StopIteration error

"""Delegating Iterators"""

from collections import namedtuple

Person = namedtuple("Person", 'first last')

class PersonNames:

    def __init__(self, persons):
        try:
            self._persons = [person.first.capitalize() 
                            + " " + person.last.capitalize()
                            for person in persons]

        except (TypeError, AttributeError):
            self._persons = []

    def __iter__(self): # Since self._persons is a list, we can return it's iterator by passing it through an iter function. This is called as deligating iterators.
        return iter(self._persons) 

persons = [Person("pulkit", "agrawal"), Person("Aanisha", "mishra"), Person("gauri", "agrawal")]

person_names = PersonNames(persons)
result = person_names._persons  #return ['Pulkit Agrawal', 'Aanisha Mishra', 'Gauri Agrawal']

#we can iterate thorugh this as well.
[names for names in person_names] #return ['Pulkit Agrawal', 'Aanisha Mishra', 'Gauri Agrawal']

"""Reverse Iteration on a Iterable"""

_SUITS = ("Spades", "Hearts", "Diamonds", "Clubs")
_RANKS = tuple(range(2, 11)) + tuple('JQKA')

from collections import namedtuple

Card = namedtuple("Card", "rank suit")

class CardDeck:
    def __init__(self):
        self.length = len(_SUITS) * len(_RANKS)
    
    def __len__(self):
        return self.length
    
    def __iter__(self):
        return self.CardDeckIterator(self.length)
    
    class CardDeckIterator: 
        def __init__(self, length):
            self.length = length
            self.i = 0 

        def __iter__(self):
            return self 
        
        def __next__(self):
            if self.i >= self.length:
                raise StopIteration
            else:
                suit = _SUITS[self.i // len(_RANKS)]
                rank = _RANKS[self.i % len(_RANKS)]
                self.i +=1
                return Card(rank, suit) 

deck = CardDeck()

#let's say now we want the last 5 values, one way to do it is this:
result = list(deck)[:-6:-1]
#but this is very wateful because we had to generate the entire list of card deck in order to utilise the last 5

#Solution: 
#In general python has this built in reverse function which returns an iterator, for example

l = [1,2,3,4]
result = reversed(l)  #returns <list_reverseiterator object at 0x00000196A5858A20> which we can use to iterate in the reverse order.
result = list(reversed(l))  # returns [4, 3, 2, 1]

#we can also write a __reverse__ method in our class to do the same: 
_SUITS = ("Spades", "Hearts", "Diamonds", "Clubs")
_RANKS = tuple(range(2, 11)) + tuple('JQKA')

from collections import namedtuple

Card = namedtuple("Card", "rank suit")

class CardDeck:
    def __init__(self):
        self.length = len(_SUITS) * len(_RANKS)
    
    def __len__(self):
        return self.length
    
    def __iter__(self):
        return self.CardDeckIterator(self.length)

    def __reversed__(self):
        return self.CardDeckIterator(self.length, reverse = True)
    
    class CardDeckIterator: 
        def __init__(self, length, reverse = False):
            self.length = length
            self.reverse = reverse
            self.i = 0 

        def __iter__(self):
            return self 
        
        def __next__(self):
            if self.i >= self.length:
                raise StopIteration
            else:
                if self.reverse:
                    index = self.length -1 - self.i
                else:
                    index = self.i 
                suit = _SUITS[index // len(_RANKS)]
                rank = _RANKS[index % len(_RANKS)]
                self.i +=1
                return Card(rank, suit) 

deck = CardDeck()

[cards for cards in reversed(deck)] #you will get a reversed list of cards

"""
we don't need to define this __reversed__ method for sequence type, but then it is cumpulsory to define the __len__ method, for the python reversed fucntion to work
Pyton basically start using the __getitem__ method, but instead start passing [len(obj)-1- i] as an argument. 

"""

class Squares:
    def __init__(self, length ):
        self.squares = [i**2 for i in range(length)]

    def __len__(self):
        return len(self.squares)
    
    def __getitem__(self, s):
        return self.squares[s]

sq = Squares(5)

sq_list = list(sq) #return [0, 1, 4, 9, 16]
sq_reversed = list(reversed(sq)) #return [16, 9, 4, 1, 0]