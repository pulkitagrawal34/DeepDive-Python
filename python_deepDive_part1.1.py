# python --version : 3.7.3
'''
Content Covered in this module:
1. Quick refresh of basics of Python 
1. Python variable and Memory reference 
2. Numeric Data Types 
'''

# #try ...except...finally

# a = 0
# b = 10

# while a<4:
#     print("-----------------------")
#     a+=1
#     b-=1

#     try: 
#         a/b
#     except ZeroDivisionError:
#         print("{0}, {1}- division by 0".format(a,b))
#         break
#     finally:
#         print("{0}, {1} - this always executes".format(a,b))

#     print("{0}, {1} - main loop".format(a,b))
# else:
#     print("code executed smoothly")


#-----------------------------------

# classes in python 

class Rectangle: 
    def __init__(self, width, height):
        self.width = width 
        self.height = height 
    
    def __str__(self):
        return "Rectange: width = {0}, height = {1}".format(self.width, self.height)
    
    def __repr__(self):
        return 'Rectange({0}, {1})'.format(self.width, self.height)

    def __eq__(self, other): #equal to method 
        if isinstance(other, Rectangle): #to check that the object we are comparing it with is also a Rectangle
            return (self.width, self.height) == (other.width, other.height)
        else:
            return False

    def __lt__(self, other): #less than method
        if isinstance(other, Rectangle):
            return self.area() < other.area()
        else:
            return NotImplemented
    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2*(self.width + self.height)

#how to use getters and setters in classes

class Rectangle_V2:
    def __init__(self, width, height):
        self.width = width 
        self.height = height 
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self,width):
        if width<=0:
            raise ValueError("width must be positive")
        else:
            self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self,height):
        if height<=0:
            raise ValueError("height must be positive")
        else:
            self._height = height

    def __str__(self):
        return "Rectange: width = {0}, height = {1}".format(self.width, self.height)
    
    def __repr__(self):
        return 'Rectange({0}, {1})'.format(self.width, self.height)

    def __eq__(self, other):
        if isinstance(other, Rectangle):
            return (self.width, self.height) == (other.width, other.height)
        else:
            return False



#variables and Memory 

import sys 
import ctypes 
def ref_count(address: int):#to see number of variables pointing to that address
    return ctypes.c_long.from_address(address).value
 
a = [1,2,3]
  
# print(id(a))
# print(sys.getrefcount(a)) #will always return +1 count because at the moment, this func is also pointing to that memory location 
# print(ref_count(id(a)))


#GARBAGE COLLECTOR 
import gc

#To check if garbage collector has an eye on that memory location
def object_by_id(object_id):
    for obj in gc.get_objects():
        if id(obj) ==object_id:
            return "object exists"
    
    return "Not found"

#creating a circular reference 
class A:
    def __init__(self):
        self.b = B(self)
        print("A: self : {0}, b:{1}".format(hex(id(self)), hex(id(self.b))))

class B:
    def __init__(self, a):
        self.a = a 
        print("B: self : {0}, a:{1}".format(hex(id(self)), hex(id(self.a))))

#disable the garbage collector
# gc.disable()

# my_var = A()

# #storing the memory locations 
# a_id = id(my_var)
# b_id = id(my_var.b)

# print(ref_count(a_id)) # should return 2 because both my_var and B is referring to A
# print(ref_count(b_id)) # should return 1

# print(object_by_id(a_id))
# print(object_by_id(b_id))

#setting the my_var reference to None
# my_var = None 

# print("my-var has beene set to None")
# print(ref_count(a_id)) # should return 1 
# print(ref_count(b_id)) # should return 1

# print(object_by_id(a_id))
# print(object_by_id(b_id))

# print("Manually running the garbage collector")
# gc.collect()

# print(ref_count(a_id))
# print(ref_count(b_id))

# print(object_by_id(a_id))
# print(object_by_id(b_id))


#EVERYTHING IS AN OBJECT

def square(s):
    return s**2

def cube(c):
    return c**3


def select_func(fn_id):
    if fn_id ==1:
        return square 
    else:
        return cube 


f = select_func(2)
f(10)

#we can pass the value "10" like this as well 
f_ = select_func(2)(10)  #this will pass the value 10 to the return function(cube/aquare) depending upon the func_id


#PYHTON OPTIMIZATIONS :Interning

#forcing a string to intern

import sys 

a = sys.intern("your text here")
b = sys.intern("your text here")

a is b #would return True

#If a string is interned we can simply compare their memeory address instead of comparing it character by character.

def compare_using_equals(n):
    a = 'a long string that is not interned' *200
    b = 'a long string that is not interned' *200
    
    for i in range(n):
        if a == b :
            pass

def compare_using_interning(n):
    a = sys.intern('a long string that is not interned' *200)
    b = sys.intern('a long string that is not interned' *200)
    
    for i in range(n):
        if a is b :
            pass


# compare_using_equals(10000000) # implemented in 3.49s
# compare_using_interning(10000000) #implemented in 0.42 sec


#PYTHON OPTIMISATIONS

#python precalculates expressions results and store it so that 
#it doesn't have to do that calculation again and again.
def my_func():
    a = 24 * 60
    b = (1,2) * 5
    c = "abc" * 3
    d = "ab" * 11
    e = "The quick brown fox " * 5 
    f = ["a", "b"] *3

# print(my_func.__code__.co_consts)

def search_element(e):

    if e in [1,2,3]: # python converts this list into tuple for faster processing. 
        pass         # similarly sets gets converted to --> frozenset

# print(search_element.__code__.co_consts)


#set vs list/tuple membership

import string 
import time

char_list = list(string.ascii_letters)
char_tuple = tuple(string.ascii_letters)
char_set = set(string.ascii_letters)

def membershipTest(n, container):
    for i in range(n):
        if "z" in container:
            pass

# membershipTest(10000000, char_list) # 4.82 sec
# membershipTest(10000000, char_tuple) # must be close to list timings
# membershipTest(10000000, char_set) #0.84 sec


#INTEGERS DATA TYPE

#constructor and bases 

a = int() #initialised with default value 0
a = int(True) # returns 1 for True and 0 for False

#we can also initialise it with a string and base 
a = int("97") # default base is 10, if not specified
a = int('1010', base = 2) # 1010 is base 2 representation of integer 10
a = int("a", base= 16) #hexadecimal representation of 10

#code to represent an integer from base 10 ---> base b 

def from_base10(num, b:int):
    if b < 2 or b >36:
        raise ValueError("Base b must be 2 <= b <=36")

    if num == 0:
        return 0 

    sign = -1 if num <0 else 1
    num*= sign

    mapping = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    #key concept:
    # numberator/denominator  = (numerator//denominator) * denominator + numerator%denominator

    encoding = []

    while num >  0 :
        m = num % b
        num = num // b
        encoding.insert(0,m)

    encoded =  "".join([mapping[i] for i in encoding])
    
    if sign == -1:
        encoded = "-" + encoded

    return encoded

# result = from_base10(3451,16)
# print(result)
# print(int(result, base= 16))


# RATIONAL NUMBERS

from fractions import Fraction 
import math 
x = Fraction(3, 4)
y = Fraction(6, 8)

# print(x ==y) # return True because Fractions are automatically reduced Fraction(6,8) -- > fraction(3,4)
# print(x.numerator)
# print(x.denominator)

""" 
Constructor
1. Fraction(numerator = 0, denominator = 1)
2. Fraction(other_fraction)
3. Fraction(float) #floats have finite level of precision
4. Fraction(decimal) 
5. Fraction(string)   # Fraction ('22/7') --> Fraction(22, 7)
                        Fraction('10') --> Fraction(10, 1)
                        Fraction("0.125) -- > Fraction(1, 8 )
"""

x = Fraction(math.pi) 
# print(x) #would return 884279719003555/281474976710656 which is an approximation of the irrational number pi as internally irrational numbers are stored as float.


y = Fraction(0.3)
# print(y) # would return Fraction(5404319552844595, 18014398509481984) 

#This happens because in reality python stores 0.3 as :
format(0.3, '0.25f')  #returns 0.2999999999999999888977698

"""In order  to avoid this we can limit the denominator
This would force python to find a number which is closest to 0.2999999999999999888977698 and can be represented with the limiting denominator"""
y.limit_denominator(10) # return Fraction(3, 10)
x.limit_denominator(10) # return Fraction(22, 7)


#Floats 

#equality testing in float 

x = 0.1
format(x, '0.25f') # 0.1000000000000000055511151
#this happens because not all floats can be represented exactly in binary representation

#let, 
x = 0.125 + 0.125 + 0.125
y = 0.375
x==y # returns True 

#but, if :
x = 0.1 + 0.1 + 0.1
y = 0.3
x==y  # returns False 

#the way we can address this problem by definiting an absolute_tolerance "ε"such that |x - y| < ε
#But the problem arises when numbers are too close to zero or too far from zero 
#for example

def equality_check(num1 , num2, absolute_tolerance):
    return  math.fabs(num1- num2) < absolute_tolerance

x = 0.01
y = 0.02

equality_check(x, y, 10e-17) # returns False 

#but let's say, 
x = 10000.01
y = 10000.02

#They are pretty close, but, 
equality_check(x, y, 10e-17) # returns False 

#Hence we need to use a relative tolerance instead of an absolute one but that too alone would not work in situations where the values of x and y are close to zero 
#hence we combine them as follows:

def equality_check2(num1, num2, relative_tolerance, absolute_tolerance):
    tolerance = max(relative_tolerance * max(math.fabs(num1), math.fabs(num2)), absolute_tolerance)
    return math.fabs(num1-num2) < tolerance

#Python has an inbuilt method which does this eaxctly same thing for us : isclose()

from math import isclose

#isclose(a, b , rel_tol = 1e-9, abs_tol = 0.0)--> bool
x = 0.1 + 0.1 + 0.1
y = 0.3

isclose(x, y) # returns True 
x== y # returns False 

x = 123456789.01
y = 123456789.02
isclose(x, y, rel_tol = 0.01)  # returns True, looks good. 

#But, lets take another scenario 
x = 0.0000001
y = 0.0000002
isclose(x, y, rel_tol = 0.01) #returns False 

#So we need to adjust the values of abs_tol and rel_tol in a way such that it works for either scenario 

x1 = 123456789.01
y1 = 123456789.02

x2 = 0.0000001
y2 = 0.0000002

isclose(x1, y1 , rel_tol = 0.01, abs_tol = 0.01) #returns True
isclose(x2, y2 , rel_tol = 0.01, abs_tol = 0.01) #returns True

#FLOATs ----> Integers 

#Truncation ---> Takes away the decimal part 
math.trunc(10.4) # returns 10
math.trunc(-10.4)# returns -10 
# or int(10.4), int(-10.4) would also  return 10, -10

#Floor --> small integer <= number 
math.floor(10.4) # returns 10
math.floor(-10.4) # returns -11

#ceiling -- > small integer >= number 
math.ceil(10.4) #returns 11
math.ceil(-10.4) #returns -10

#Round   
#round(x, n= 0) --> rounds a number x to the closest multiple of 10**(-n) 
#for n = 0 , rounds to closest multiple of 10**(-0) i.e. 1 
#for n = 1 , rounds to closest multiple of 10**(-1) i.e. 0.1 
#for n = -1, rounds to closest multiple of 10**(-(-1)) i.e. 10

round(10.6, 0) #returns 11.0
round(18.5, -1)  # returns 20  
round(888.88, -1) # return 890.0
round(888.88, -2) # return 900.0
round(888.88, -4) # return 0.0 

#Rounding a tie Breaker
round(1.25, 1) # returns 1.2 # round it to the nearest value with an EVEN least significant digit
round(-1.25, 1) # returns -1.2 # round it to the nearest value with an EVEN least significant digit

#for, 
round(1.35, 1)  # returns 1.4 
round(-1.35, 1)  #  returns -1.4

#similarly
round(1.5, 0)  # returns 2.0
round(2.5, 0)  # returns 2.0 
round(3.5, 0)  # returns 4.0 

#incase we always want to round away from zero in case of a tie breaker 

def round_up(x):
    from math import copysign 
    return int(x + 0.5* copysign(1, x))

round_up(1.5)   # returns 2
round_up(2.5)   # returns 3 
round_up(3.5)   # returns 4 

"""Decimals"""

import decimal 
from decimal import Decimal 

"""
Constructor 

Integers  a = Decimal(10) 
String    a = Decimal("0.1")
Tuples    a = Decimal((1, (1, 2, 3), -2))
Float     a = Decimal(0.1)  "BIG NO NO" because the decimal will store the actual 
                            value of 0.1 which is 0.1000000000000000055511151231257827021181583404541015625
"""
# Working with Tuples constructor
# 1.23 = +123 * 10**-2  --> (sign, (d1, d2, d3), exp)  --> s = 0 if x>=1 else 1

a = Decimal((1, (1, 2, 3), -2))   # return -1.23
a = Decimal((0, (1, 2, 3), -2))   # return  1.23

#context precision and the constructor 

a = Decimal('0.12345')
b = Decimal('0.12435')

c = a+b # returns 0.24780

with decimal.localcontext() as ctx:
    ctx.prec = 2 #setting this to 2 would not affect storange but it will affect the arithmetic expression 
    c = a + b  #returns 0.25

c = a + b # back to 0.24780

#mathematic operations 

# 1. // and % operators in decimal are slightly different but It still satisfy n = d* (n // d) + n % d 

x = 10 
y = 3 
x//y  # returns 3 
x % y  # returns 1 
divmod(x, y) # returns (3, 1)
(x == y* (x // y) + x % y) # returns True 

x = Decimal(10)
y = Decimal(3) 
x//y  # returns 3 
x % y  # returns 1 
divmod(x, y) # returns (3, 1)
(x == y* (x // y) + x % y) # returns True 

x = Decimal(-10)
y = Decimal(3) 
x//y  # returns -3  #here trunc(x//y) happens instead of math.floor(x//y) like in the case of integers 
x % y  # returns -1 
c, d  = divmod(x, y) # returns (3, 1)
(x == y* (x // y) + x % y) # returns True 

#logarithmic, exponent and square root is implemented differntly by Decimal as compared to math

a = Decimal('1.5')
a.ln()
a.exp()
a.sqrt()

#Note: If we use math module, it first converts the Decimal type to float and then performs the mathematical operation. 
math.sqrt(a) == a.sqrt() # return False 

#BOOLEANS -- >they are integer subclass  True --> 1,  False -->0, However they don't share the memory address

issubclass(bool, int) # returns True
isinstance(True, bool) # returns True 
isinstance(True, int) # returns True

int(True) # returns 1
int(False) #returns 0 

True is 1 # returns False 
True == 1 # returns True 

# we can implement arithmetic operations on bool just like integers
True + True # returns 2 

#All objects in python have an associated Truth value

#example for Integers 
def __bool__(self):
    return self!=0 

#bool(x) ---> calls x.__bool__() method and returns True or False 

a = bool(Fraction(0, 1)) #returns False because 0/1  ==0
b = bool(Decimal('0.0')) #returns False
c = dict()
d = set()
bool(c) #returns False because they are empty 
bool(d) #returns False because they are empty 

#Note: bool returns False if value ==0  or len(object) == 0 

#real time use case 

my_list = [1,2,3]

if my_list is not None and len(my_list) > 0 :
    pass

# the above code can be re-written as 
if my_list:   #python is esentially looking at bool(my_list)
    pass

a = 0 
total = 10 
x = a and total/a
x # returns 0

'''
Definition of "or" and "and" in python / concept of shot-circuiting
X or Y : If X is truthy, return X, otheriwise evaluate y and return it.  
X and Y: if X is falsy, return X, otherwise evaluate Y and return it. 
'''

"a" or [1,2]  #returns "a"
""  or [1,2]  # returns [1,2]

1 or 1/10 # returns 1
#0 or 1/0 # returns ZeroDivisionError

s1 = None
s2 = ""
s3 = "abc"

#if we don't want None or an empty string
s4 = s1 or s2 or s3
# print(s4) returns "abc"
