#Python -version: 3.7.3
"""
This Module covers:
1. Functions and Parameters 
2. Positional unpacking and iterables
3. Fist class Functions
"""

def myfunc(a, b , c):
    return "a = {0}, b = {1}, c = {2}".format(a,b,c)

myfunc(1,2,3) # returns a = 1, b = 2, c = 3

def my_func(a, b= 2 , c= 3): #Once you start assigning default values, you must assign it for all the functions' parameters after that.
    return "a = {0}, b = {1}, c = {2}".format(a,b,c)

my_func(10) # returns a = 10, b = 2, c = 3, since we have defined a deafault valuesfor b and c , the arguments are optional.

my_func(c = 30, b = 20, a = 25) # returns a = 25, b = 20, c = 30, Position is irrevelent, but keyword must match the parameter name

#we can even write it as a combination of positional and keyword argument
my_func(10, c = 30, b = 20) # returns a = 10, b = 20, c = 30


"""
POSITIONAL UNPACKING AND ITERABLES
"""
#TUPLES

a = 1,2,3
type(a) # returns tuples 

#Note: A tuple is not defined by it's parenthesis but by "comma"(,), although we can use the parenthesis to create an empty tuple

# Thi is  how you can define a tuple with a single element 
a = 1, 
# print(a)  # returns (1, )
# here the parenthesis are just for the display.

a, b , c  = [1, "a", 3.14]
#This is called as positional unpacking
a  #returns 1  
b  #returns "a"  
c  #returns 3.14

#  Interchanging values of elements can simply be done as: 
a = 10 
b = 20 

a, b = b, a
a # returns 20
b # returns 10
#The point to note here is that python evaluates the right hand side of the above euation first, so (b, a) -- > (20, 10) and then it does the assignemnt. 

# we can impplement it for all the iterable objects in python 
my_dict = {"a": 1, "b": 2, "c": 3, "d": 4}

var1, var2, var3, var4 = my_dict  
var1 # retruns "a"
var2 # retruns "b"
var3 # retruns "c"
var4 # retruns "d"

#Note : In case of dictionary we get back the keys, but dictionaries are unordered, so positional order is not guranteed.
#In case we want the values we call the my_dict.values() method or my_dict.items() for both keys and values

"""
Unpacking using *expression for unpacking
"""
#using it on the LHS
my_list =[1,2,3,4,5,6,7,8]

a, *b = my_list 
a # returns 1
b # returns [2,3,4,5,6,7,8] # always returns a list

s = "python"
a, *b = s 

a # returns "p"
b # retruns ['y', 't', 'h', 'o', 'n']

my_list =[1,2,3,4,5,6,7,8]
a, *b , c = my_list
a # returns "p"
b # returns  ['y', 't', 'h', 'o']
c # returns "n"

#or, if we want first two and the last element. 
s = "python"
a , b , *c , d = s #
#Note: Be careful while using this with sets, as their is no positional ordering 

"""
using * expression on RHS
"""
l1 = [1, 2, 3]
l2 = [4, 5, 6]
l = [*l1, *l2]   # retruns [1, 2, 3, 4, 5, 6]

#we can use any iterable object, {string, list, tuples, sets, dictionary....anything}
l1 = [1,2,3]
l2 = {4,5,6}
l = [*l1, *l2]  # return [1, 2, 3, 4, 5, 6]
l = {*l1, *l2}  # returns {1, 2, 3, 4, 5, 6} --> will remove any repeated value, if present. 

s1 = "abc"
s2 = "cde"
s = {*s1, *s2}  # returns {'e', 'd', 'a', 'b', 'c'}

#Really beneficial to combine sets
s1 = {1, 2, 3}
s2 = {3, 4, 5}
s3 = {5, 6, 7}
s4 = {7, 8, 9}

s = {*s1, *s2, *s3, *s4}  # returns {1, 2, 3, 4, 5, 6, 7, 8, 9}
s = [*s1, *s2, *s3, *s4] # returns [1, 2, 3, 3, 4, 5, 5, 6, 7, 7, 8, 9]

# can be used for dictionaries as well

d1 = {"key1": 1, "key2": 2}
d2 = {"key2": 3, "key4": 4}

d5 = {*d1, *d2}  # returns {'key2', 'key1', 'key4'}
d3 = {**d1, **d2} # returns {'key1': 1, 'key2': 3, 'key4': 4}
d4 = {**d2, **d1} # returns {'key2': 2, 'key4': 4, 'key1': 1}  

# Note: Here since a dictionary has unique keys, the dictionary added later will be given a preference. 

"""Nested Unpacking """
a, b, e = [1, 2, "xy"]  # returns a=1, b = 2, e = "xy"
c, d = e # returns c= "x", d = "y"

#Instead we can use a nested unpacking 
a, b , (c, d) = [1, 2 , "xy"]  # returns 1,  2,  x,  y

#we can also use it as:
a, *b, (c,*d) = [1,2,3,4,5,"python"]  # returns 1, [2, 3, 4, 5],  p,  ['y', 't', 'h', 'o', 'n']

""" *args in function"""

def func1(a, b , *args):
    return a,b,args

result = func1(1, 2, 3)  # retruns 1, 2, (3,)
result = func1(1, 2)  # retruns 1, 2, ()
result = func1(10, 20, 1, 2, 3)   # returns (10, 20, (1, 2, 3))

def avg(*args):
    count = len(args)
    total = sum(args)
    return total/count

result = avg(1,2,3) # returns 2
result = avg(1,2,3,4,5,6,7,8,9) # returns 5.0

#result = avg()   # This will throw a  zero division error if we pass no argument while calling the function
#hence we can use short-circuiting to avoid the zero division error
def avg(*args):
    count = len(args)
    total = sum(args)
    return count and total/count

#Passing values from a list as an input to the function
arguments = [10, 20, 30, 40, 50]

#result = avg(l) #if we pass it directly it will throw an error, instead we can unfold it first and then pass as an argument
result = avg(*arguments)  # returns 30.0

#or, lets sa y you have a function
def func2(a, b , c, *args):
    return a, b , c , args

result = func2(*arguments)  # returns 10, 20, 30, (40, 50)

"""Keyword arguments"""

def func3(a, b , *args, d): # Though *args exhausts all positonal arguments,  we can pass arguments here is by providing named arguments
    return a, b , args, d

result = func3(1, 2, "x", "y", d = 100) 
result = func3(1, 2, d= 100)  # returns 1,2, (), 100
#Note:
#result = func3(1,2)  # this will throw an error--> "func3() missing 1 required keyword-only argument: 'd'"

def func4(*args, d):
    pass
    
result = func4(1,2,3, d = 100) #args = (1,2,3), d = 100
result = func4(d = 100)  # args = (), d = 100
# print(result)

def func5(a, b=20, *argv, d = 0, e): 
    return a, b, argv, d, e
'''
Note: In general,Once you start passing a default value parameter in a function, you have to pass a default value for all the other parameters coming after it
for example:
    def func(a, b = 2, c= 3):
        pass 
 Here I have to pass to a default value to c. 

 But In case we are passing *argv after a default valaue parameters such as b =20, you need not pass a default value parameter, because it is compulsory to 
 pass a keyword only arguments for parameters after *argv during a fucntion call . 
'''

# result = func5(5, 4 ,3, 2, 1)  --> This will throw an error because e is undefined and also has no default value.
result = func5(5, 4 ,3, 2, 1, e = "all engines running")  # returns 5, 4, (3, 2, 1), 0, 'all engines running'
result = func5(0, 600, d = "good morning", e = "python")  # returns 0, 600, (), 'good morning', 'python'

''' **kwargs : short for "variable key word argument" '''


def func(**kwrgs):
    return kwrgs

result = func(a = 1, b = 2, c = 3)  # returns {'a': 1, 'b': 2, 'c': 3}

#you can also define, 
def func(*args, **kwrgs): 
    return args, kwrgs

result = func(1, 2, a = 100, b = 200)  # returns (1, 2), {'a': 10, 'b': 20}

"""Building a Functional Timer"""

import time 

def time_it(fn, *args, rep = 1,  **kwargs):
    start = time.time()
    for i in range(rep):
        fn(*args, **kwargs) # unrapping it before passing it through function

    return (time.time()-start)/rep

# time_it(print, 1, 2, 3, sep= ' - ', end = " *** \n", rep = 5)


"""Default values, beware!!!!"""

from datetime import datetime

def log(msg, dt = datetime.utcnow()):
    return "{0}, {1}".format(dt, msg)

log("message 1") # return 2020-07-19 15:06:22.1306979, message 1
# time.sleep(1)
log("message 2") # returns 2020-07-19 15:06:22.1306979, message 2

"""Notice that here we got the same datetime value returned because when we ran this module, a default value got assigned to keyword parameter-->"dt" in log function 
and if the keyword argumnet is not provided while calling the function, it will return the deafult value assigned at the time of creation, so it will never change
until manually specified, the hence In order to avoid situations like this: """

def log(msg, dt = None):
    dt = dt or datetime.utcnow()
    return "{0}, {1}".format(dt, msg)

log("message 1") # return 2020-07-19 15:07:00.601411, message 1
# time.sleep(1)
log("message 2") # return 2020-07-19 15:07:01.602570, message 2

"""Docstrings and Annotations: Meta data attached to the functions"""

def myfunc(a, b=1):
    """ 
    returns a * b   

    Additonal Documents:

    Inputs :

    Outputs: 
    """
    return a *b

#docstrings must be the first line of code in order to be part of the documentation

myfunc.__doc__

def my_func(a:"annotation for a", b:"annotation for b" = 1) -> "something":
    """ Documentation for my function """
    return a * b

my_func.__doc__ #returns  Documentation for my function
my_func.__annotations__  # returns {'a': 'annotation for a', 'b': 'annotation for b', 'return': 'something'}


x = 10 
y = 5

def myfunc(a: "some character", 
           b: "maximum between x and y" = max(x, y)) -> "returns a repeated " + str(max(x, y)) + " times":
    return a * max(x, y )

myfunc("a") # returns aaaaaaaaaa i.e. "a" 10 times 
myfunc.__annotations__ # returns {'a': 'some character', 'b': 'maximum between x and y', 'return': 'returns a repeated 10 times'}

#Notice that if we now change the value of x to 20, the annotations still remain the same, but they were assigned when the function was created. 
x = 20 

myfunc("a") # returns aaaaaaaaaaaaaaaaaaaa i.e. "a" 20 times 
myfunc.__annotations__ # returns {'a': 'some character', 'b': 'maximum between x and y', 'return': 'returns a repeated 10 times'} 

"""Lambda Expressions and Sorting(als called highe rorder function because it can take a function as an argumentx) """

l = ["c", "B", "D", "a"]

sorted(l) # return ["B", "D", "a", "c"] because the ascii value of "B" is smaller than "a"

#here we can use lambda expression to avoid this
sorted(l, key = lambda x: x.upper(), reverse = False) # return ['a', 'B', 'c', 'D']
""" The sorted function sorts the output of the lambda function"""

mydict = {"a" : 97, 
          "b": 200, 
          "c": 36}

sorted(mydict.items(), key = lambda x: x[1], reverse = True) #returns [('b', 200), ('a', 97), ('c', 36)]

sorted(mydict, key = lambda x: mydict[x], reverse = True) # returns ['b', 'a', 'c']

#we can pass any function to the "key" paramter in sorted function. 
def dist_sq(x):
    return (x.real)**2 + (x.imag)**2

l = [3+3j, 1-1j, 3+0j]
sorted(l, key = dist_sq, reverse = False) # returns [(1-1j), (3+0j), (3+3j)]
sorted(l, key =lambda x: (x.real)**2 + (x.imag)**2, reverse = False) # returns [(1-1j), (3+0j), (3+3j)]

"""Map and Filters  : They are higher order functions

Map( func, *iterables) : returns an iterator, we can either pass it through a list or run a for loop to produce results. 

Filter(func, iterable)--> will return a iterator that contain all the elements of the iterable for which the function called on it is Truthy.
If the function is None, it simply returns the elements of the iterables that are Truthy.

"""
mylist = [2,3,4]

def sq(x):
    return x**2

list(map(sq, mylist))  # returns [4, 9, 16]
list(map(lambda x: x**2, mylist))  # returns [4, 9, 16]

mylist1 = [1,2,3]
mylist2 = [10,20,30]

def add(x, y):
    return x + y 

a = list(map(add, mylist1, mylist2))  # returns [11, 22, 33]
a = list(map(lambda x, y : x + y , mylist1, mylist2))  # (using lambda function) returns [11, 22, 33]

#filters 

mylist = [0,1,2,3,4,5]

a = list(filter(None, mylist)) # returns [1, 2, 3, 4, 5]
a = list(filter(None, [1, 0, 4, "a", "", None, True, False])) # returns [1, 4, 'a', True]

def is_even(x):
    return x %2 ==0

a = list(filter(is_even, mylist)) # returns [0, 2, 4]
a = list(filter(lambda x: x % 2== 0, mylist))  # (using lambda function) returns [0, 2, 4]

""" Reducing Functions"""

_max = lambda x, y : x if x > y else y

def max_sequence(sequence):
    result = sequence[0]
    for i in sequence[1:]:
        result = _max(result, i )

    return result 

_min = lambda x, y : x if x < y else y

def min_sequence(sequence):
    result = sequence[0]
    for i in sequence[1:]:
        result = _min(result, i )

    return result 

_add = lambda x, y : x+y 

def add_sequence(sequence):
    result = sequence[0]
    for i in sequence[1:]:
        result = _add(result, i )

    return result 

mylist = [5, 3, 6, 10, 9]

a = max_sequence(mylist) # returns 10
a = min_sequence(mylist) # returns 3
a = add_sequence(mylist) # returns 33

#We can clearly see that all the above functions only have a slight difference, henvce we can write a generic _reduce function as:
def _reduce(fn, sequence):
    result = sequence[0]
    for x in sequence[1:]:
        result = fn(result, x)
    return result 

a = _reduce( lambda x, y: x+y , mylist) # returns 33
a = _reduce( _add, mylist) # returns 33

a1 = _reduce( lambda x, y: x if x > y else y , mylist) # returns 10
a1 = _reduce( _max, mylist) # returns 10

a2 = _reduce( lambda x, y: x if x < y else y , mylist) # returns 3
a2 = _reduce( _min , mylist) # returns 3

"""python has an inbuild reduce function which can be imported as following:
            from functools import reduce 

        reduce(funciton, iterable, initializer)

This reduce function works with any kind of iterables(list, set, string etc)
"""
from functools import reduce 

a = reduce(_max, mylist) # returns 10 
a = reduce(_add, {1, 2, 3, 4, 5 , 6}) # returns 10
a = reduce(lambda x, y: x * y, mylist) # returns 8100
#Can be used to calculate factorial of a number. 
a = reduce(lambda x, y: x * y, list(range(1, 5+1))) # returns 120 

s = [True, 1, 0 , None]
s1 = {False, "", 0, None}

a = any(s) # returns True  --> returns True if any value is Truthy
a = any(s1) # returns False

a = all(s) # returns False --> returns True if all the values are Truthy 
a = all(s1) # returns Flase

#we can write these reducing functions ourselves 

a = reduce(lambda x, y : bool(x) or bool(y), {True, 1, 0, None}) # returns True 
a = reduce(lambda x, y : bool(x) or bool(y), {False, "", 0, None}) # returns False 

a = reduce(lambda x, y : bool(x) and bool(y), {True, 1, 0, None}) # returns False
a = reduce(lambda x, y : bool(x) and bool(y), {False, "", 0, None}) # returns False 

#Use of Initialiser keyword argument in reduce function

mylist = [1,2,3,4]
a = reduce(lambda x, y : x + y, mylist, 100) # returns 110

#we can do this in our defined _reduce function as well
def _reduce(fn, sequence, initial_value = 0):
    result = initial_value
    for x in sequence:
        result = fn(result, x)
    return result 

a = _reduce(lambda x, y : x + y, mylist, 199 ) # returns 209

#since we are using an initialiser, we can now use any iterables here

myset = {1,2,3,4}
a = _reduce(lambda x, y : x + y, myset, 199 ) #returns 209

"""Using partial functions: used to reduce the number of argumnets required to call the function"""
from functools import partial 

def pow(number, exponent):
    return number**exponent 

square = partial(pow, exponent= 2 )
cube = partial(pow, exponent = 3 )

a = square(2) # returns 4 
a = cube(3) # returns 27

## BEWARE!!
a = cube(2, exponent = 10) # returns 1024

#we can write this partial function by ourself as well, like this:

def square(number):
    return pow(number, 2)

def cube(number):
    return pow(number, 3)

a = square(16) # returns 100
a = cube(5) # returns 125

#Application 1
#using distance from origin metric to sort a list 

origin = (0,0)

mylist = [(1,1), (0,2), (-3, 2), (0,0), (10, 10)]

dist2 = lambda a, b: (a[0] - b[0])**2 + (a[1] - b[1])**2 

a = dist2((1,1), origin) # returns 2

a = sorted(mylist, key= partial(dist2, b = origin), reverse = True ) # returns [(10, 10), (-3, 2), (0, 2), (1, 1), (0, 0)]
a = sorted(mylist, key = lambda x: dist2(x, origin), reverse = True) # returns [(10, 10), (-3, 2), (0, 2), (1, 1), (0, 0)]
