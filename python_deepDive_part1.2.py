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

def my_func(a, b= 2 , c= 3):
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
l1 = [1,2, 3]
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
a, b, e = [1, 2, "xy"]  # returns a=1, b = 2, c = "xy"
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
