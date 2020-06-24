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

result = from_base10(3451,16)
print(result)
print(int(result, base= 16))

