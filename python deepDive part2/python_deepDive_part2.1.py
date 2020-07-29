# python_deepDive part 2 
# python version: 3.7.3

"""
This module contains the following:
    1. sequences : They have "positional ordering" i.e A list is a sequence, set it not.         
            a. Shallow copy and Deep copy
            b. Slicing
            c. Creating Custom Sequences
            d. Inplace mutation-- > using "+=" or "*=" operator does a inplace mutation(for mutable iterables only) as opposed to "+" operator
    2. Iterable : It is a container type of object and we can list out the elements one by one. But the order in which they come is not guranteed.
        for example: sets are iterable but their order is not guranteed. 

"""

"""BEWARE of Concatenations"""

# x = [1, 2]       a = x + x       a - > [1,2,1,2]

# x = "python"     a = x + x       a - > "pythonpython"

#It works find if the objects inside the sequence is immutable, but lets's consider this case in which the objects inside the sequence is mutable
x = [[0, 0]]
a = x + x  # a = [[0, 0], [0, 0]]
a[0][0] = 100 

result = a #returns [[100, 0], [100, 0]]

"""This happened because, what python did is  -> whenever we concat the same value or use repeatations (for example: a = [[0, 0]] * 2), python copies the same memory 
address n times. Now in the case of immutable objects, it's safe to do so. but in case of mutable objects, it might create a bug as shown above. 
"""

"""Finding index in a sequence"""
#let's say we want to find the index of all the n present in the sequence: "gnu's not unix"

#method 1:
s = "gnu's not unix"

index_list = []
for index, element in enumerate(s):
    if element == "n":
        index_list.append(index)

index_list # return [1, 6, 11]

#Method 2
#first index 
s.index('n') #return 1 

#now the second index can be found by specifying that, python must look beyound index 1
s.index('n', 1+1) #returns 6 

#third index
s.index('n', 6+1) #returns 11
#beware!!-- > in case python fails to find the element in the sequence, it will return a ValueError :"substring not found"

"""SLICING"""

s = "python"
mylist = [1,2,3,4,5,6,7,8,9,10]

s[1:4] #returns "yth"-> includes the lower bound and ignores the upper bound
result = mylist[0:5] #returns [1,2,3,4,5]

s[-1] #returns "n"
s[0:5:-1] # this means go from 0 to 5 in steps of -1

result = s[0:5:-1] # returns "" because we can never go from 0 to 5 using negative steps, instead we can write:
result = s[5:0:-1] # returns "nohty"
result = s[5:0:-2] # returns "nhy"
result = s[::-1] # returns "nohtyp"

"""List vs Tuple"""

"""Property 1: Creation Efficiency"""

from dis import dis 
#we will compile them and dissassemble them to see how they work

# dis(compile('(1,2,3,"a")', 'string', 'eval'))

"""returns 

  1           0 LOAD_CONST               0 ((1, 2, 3, 'a'))
              2 RETURN_VALUE
"""

# dis(compile('[1,2,3,"a"]', 'string', 'eval'))

"""
returns 
  1           0 LOAD_CONST               0 (1)
              2 LOAD_CONST               1 (2)
              4 LOAD_CONST               2 (3)
              6 LOAD_CONST               3 ('a')
              8 BUILD_LIST               4
             10 RETURN_VALUE

"""

# dis(compile('(1,2,3,["a", "b", "c"])', 'string', 'eval'))

"""returns

  1           0 LOAD_CONST               0 (1)
              2 LOAD_CONST               1 (2)
              4 LOAD_CONST               2 (3)
              6 LOAD_CONST               3 ('a')
              8 LOAD_CONST               4 ('b')
             10 LOAD_CONST               5 ('c')
             12 BUILD_LIST               3
             14 BUILD_TUPLE              4
             16 RETURN_VALUE

"""

from timeit import timeit

# result = timeit("(1,2,3,4,5,6,7,8,9)", number = 10_100_000) # return  0.1725563
# result = timeit("[1,2,3,4,5,6,7,8,9]", number = 10_100_000) # return 1.1823567
#we can see that even creating List is a slower process a scompared to tuples

"""Property 2: Storage efficiency"""
import sys 

t = tuple()
prev = sys.getsizeof(t)
for i in range(10):
    c = tuple(range(i+1))
    size_c = sys.getsizeof(c)
    delta, prev = size_c- prev, size_c
    # print(f'{i+1} items: {size_c}, delta: {delta}')

"""returns 
1 items: 56, delta: 8
2 items: 64, delta: 8
3 items: 72, delta: 8
4 items: 80, delta: 8
5 items: 88, delta: 8
6 items: 96, delta: 8
7 items: 104, delta: 8
8 items: 112, delta: 8
9 items: 120, delta: 8
10 items: 128, delta: 8

We can see that there is a constant overhead in case of tuples
"""

l = list()
prev = sys.getsizeof(l)
for i in range(10):
    c = list(range(i+1))
    size_c = sys.getsizeof(c)
    delta, prev = size_c- prev, size_c
    # print(f'{i+1} items: {size_c}, delta: {delta}')

""" returns
1 items: 96, delta: 32
2 items: 104, delta: 8
3 items: 112, delta: 8
4 items: 120, delta: 8
5 items: 128, delta: 8
6 items: 136, delta: 8
7 items: 144, delta: 8
8 items: 160, delta: 16
9 items: 192, delta: 32
10 items: 200, delta: 8

We can see that the memory overhead is changing as the size of getting bigger, this is a concept of dynamic array, where additional memory over head is kept 
so that it doesn't have to add memory at every single step, but also not take up too much of the memory. 
"""
#Hence tuples are more memory efficient than list. 

"""property 3: retreving elements"""

t = tuple(range(100_000))
l = list(t)

result = timeit('t[99_999]', globals = globals(), number = 10_000)
result = timeit('l[99_999]', globals = globals(), number = 10_000)

#not much of a difference


"""shallow copy and deep copy"""

#shallow copy methods

l1 = [1,2,3]

#method 1
l1_copy = []
for item in l1:
    l1_copy.append(item)

result = l1_copy, id(l1), id(l1_copy)  #return [1, 2, 3], 2176372086792, 2176372087368

#method 2
l1_copy = [item for item in l1]
result = l1_copy, id(l1), id(l1_copy) #return ([1, 2, 3], 2745155815816, 2745155816328)

#method 3 - cannot be used with tuples, tuples don't have this copy attribute
l1_copy = l1.copy()
result = l1_copy, id(l1), id(l1_copy) #return ([1, 2, 3], 3008266148104, 3008266148680)

#method 4 
l1_copy = list(l1)
result = l1_copy, id(l1), id(l1_copy) #return ([1, 2, 3], 2796117662152, 2796120924104) 

#Note: the method 4 is not applicable in the case of tuples/strings
t1 = (1,2,3)
t1_copy = tuple(t1)
result = t1_copy, id(t1), id(t1_copy) # ((1, 2, 3), 2222501181192, 2222501181192)
#we can see that the id(t1) is same as id(t1_copy), this happens because of the immutability characterstics of tuples/strings, since they can't be mutated, 
#python reference the new variable to the same memory location where the tuple is stored.

#method 5: Slicing --> again not applicable for tuples/strings for the same reason as above
l1 = [1,2,3]
l1_copy = l1[:]
result = l1_copy, id(l1), id(l1_copy) #returns ([1, 2, 3], 2749262958024, 2749262957448)

#method 6: import copy module --> only applicable for list for same reason as above two 
import copy 
l1 = [1,2,3]
copy_l1 = copy.copy(l1)
result = l1_copy, id(l1), id(l1_copy) #returns ([1, 2, 3], 2575632600136, 2575632599880)


"""Deep Copies"""

#problems with shallow copy: we don't get a totally dis-associated object, there are still shared memory references. 

v1 = [0,0]
v2 = [0,0]

line1 = [v1, v2]

#let's try to use the copy method to copy the lists 
line2 = line1.copy() # or copy.copy(line1) --> same thing 

result = id(line1), id(line2)       #returns (2145950600264, 2145950564616)--> they are referencing different memory addresses
#but,
result = id(line1[0]), id(line2[0]) #returns (2535514541384, 2535514541384) -->> they are same 
result = id(line1[1]), id(line2[1]) #returns (2832309325064, 2832309325064) -->> they are also same
"""which means although line1 and line2 are pointing to a different memory address, the object inside them are pointing to the same memory location 
so if we modify the objects inside any one of them, the affect would be observed in both """

line2[0][0] = 100
result = line1, line2 #return ([[100, 0], [0, 0]], [[100, 0], [0, 0]])

#solution 1

line2 = [v.copy() for v in line1]

result = id(line1), id(line2)        #returns (2957614943816, 2957614914824)
result = id(line1[0]), id(line2[0])  # returns (2767432945352, 2767432916168)
result = id(line1[1]), id(line2[1])  # returns (2938318917192, 2938318888008)
#This works because we made a copy of the individual objects before adding it to the list2

#but let
v1 = [1,1]
v2 = [2,2]
v3 = [3,3]
v4 = [4,4]

line1 = [v1, v2]
line2 = [v3, v4]

plane1 = [line1, line2] # now we have three level of nesting 

#let's try to use the above method to make a copy of this list
plane2 =  [line.copy() for line in plane1]

result = plane1, id(plane1), id(plane1[0]) #returns ([[[1, 1], [2, 2]], [[3, 3], [4, 4]]], 2059684748936, 2059688124936)
result = plane2, id(plane2), id(plane2[0]) #returns ([[[1, 1], [2, 2]], [[3, 3], [4, 4]]], 2248084692552, 2248084692488)
#everything looks fine so far, but now if we look at the id's of the v1, v2, v3, v4 in plane1 and plane2

result = id(plane1[0][0]), id(plane1[0][1]), id(plane1[1][0]), id(plane1[1][1]) #return (1520980317384, 1520980335944, 1520980336200, 1520983717448)
result = id(plane2[0][0]), id(plane2[0][1]), id(plane2[1][0]), id(plane2[1][1])  #return (1520980317384, 1520980335944, 1520980336200, 1520983717448)
#they are same memory address, i.e. shallow copy of line isn't sufficient.

#solution --> use deepcopy from the copy module

plane2 = copy.deepcopy(plane1)

result = id(plane1[0][0]), id(plane1[0][1]), id(plane1[1][0]), id(plane1[1][1]) #return (2217031685384, 2217031703944, 2217031704200, 2217035081352)
result = id(plane2[0][0]), id(plane2[0][1]), id(plane2[1][0]), id(plane2[1][1])  #return (2217035195720, 2217035195400, 2217035195592, 2217035195528)

#example 2: The concept of deepcopy anmd shallow copy is for all the mutable onjects like list and classes

class Point:
    def __init__(self, x, y):
        self.x = x 
        self.y = y 
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

class Line:
    def __init__(self, pi, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f'Line({self.p1.__repr__}, {self.p2.__repr__})'

p1 =  Point(0,0)
p2 =  Point(10,10)
line1 = Line(p1, p2)
line2 = copy.deepcopy(line1)
result = id(line1.p1), id(line2.p1)  # eturns (2400527078400, 2400537041496)

#Instead, if we do a shallow copy
p1 =  Point(0, 0) 
p2 =  Point(10,10)
line1 = Line(p1, p2)
line2 = copy.copy(line1)
result = id(line1.p1), id(line2.p1) #returns (2400537041888, 2400537041888) --> the id's are same


"""Slicing: They are also objects, i.e we can use a slice object to define a slice """

a = slice(0,2) 
a.start #return 0 
a.stop #return  2

mylist = [1,2,3,4,5]

#slicing method 1
mylist[0:2] #return [1,2] --> starting index is included and stop index is excluded

#slicing method 2
mylist[a] # return [1,2]

"""slicing fundamentals"""
string1 = "python"

string1[0:1] #return "p"
string1[1:1] #return ""
string1[0:600] # this will get transformed to s[0:6 i.e ==(len(string1))] --> returns "python"

#we can even do Extended slicing
string1[0:6:2] #returns "pto"
#or
s1 = slice(0,6,2)
string1[s1]  #returns "pto"

#reverse slicing
string1[3:0:-1] #returns "yth"
string1[3::-1] #returns "ythp"
string1[::-1] # "nohtyp"

#BEWARE!!!! --> sometimes you can end up with empty slicing
l[3:-1:-1] # returns ""
"""
Because for python this is equivalent to l[3: 5: -1] and it is impossible to go from 3 to 5 with a -1 steps.
why?
there are two scenario's to handle this: 
case 1: k >0, by default value of k = 1

    then if i, j > length(sequence)  --> len(sequence)
            i, j < length(sequence)  --> max(0, len(seq) +i/j)
            i is None --> i = 0 
            j is None --> j = len(sequence)

case 2 :
    k < 0 
    then if i, j > length(sequence)  --> len(sequence) -1 
            i, j < length(sequence)  --> max(-1, len(seq) + i/j) 
            i is None --> i = len(sequence) -1 
            j is None --> j = -1

since in our case k < 1, so j = max(-1, len(seq) + i) = max(-1, 6-1) = max(-1, 5)
so, l[3:-1:-1] == l[3:5:-1]
"""

#In order to avoid these mistakes, slice has an "indices" method
s = slice(1, 5)

# indices attribute takes input the length of the sequence. 
result = s.indices(10) #returns (1, 5, 1)
result = s.indices(4)  #returns (1, 4, 1)

s = slice(3, -1, -1)
result = s.indices(6) # result (3, 5, -1)

#we can even unpack the result, and pass it through range to check the indices which are getting sliced
result = list(range(*slice(0,100,2).indices(10))) #return [0, 2, 4, 6, 8]

#In general, we can use it as this: 
start = 5 
stop = 10 
step = 2
length = 100 

result = list(range(*slice(start, stop, step).indices(length))) #return [5, 7, 9]

"""
Replacing a Slice : All the asignments result in an inplace mutation

- a slice can be replaced with another iterable
- for regular slices(non-extended), the slice and the iterable need not be of same length. 
- for extended slicing, the iterable and iterable must be of same length.
- Deletion is a special case of replacing a slice with an empty iterable.
- Insertion is possible too, the trick is that the slice must be empty, otherwise it would just replace the elements in the slice. 

"""
l1 = [1,2,3,4,5]
id(l1) # 1883311161992

#replacing 
l1[1:3] = "python"
l1, id(l1) #return [1, 'p', 'y', 't', 'h', 'o', 'n', 4, 5], 1883311161992
#note that the id is same, hence it is an inplace mutation 

#deletion 
l1 = [1,2,3,4,5]
id(l1) # 1576179194952

l1[2:5] = [] #we could have also used an empty string/set, any iterable would work. 
l1, id(l1)   #return [1, 2],  1576179194952 -- >again, we can see inplace mutation

#Insertion
l1 = [1,2,3,4,5]
id(l1) # 1576184758792

l1[1:1] = "insert" # this worked because slice(n,n) would always return an empty list but the starting point is still at index "n", through which we can do the insertion 
l1, id(l1)  #return  [1, 'i', 'n', 's', 'e', 'r', 't', 2, 3, 4, 5], 1576184758792 

#extended replacement 
l1 = [1,2,3,4,5]
id(l1) # 1576179194952

l1[0:5:2] = "abc" #the iterable must be of same length as the slice.
l1, id(l1)  #return ['a', 2, 'b', 4, 'c'], 1576179194952

"""Creating Custom Sequence types"""
#part 1: Immutable sequence types

class Silly:

    def __init__(self, n):
        self.n = n
    
    def __len__(self):
        self.n 

    def __getitem__(self, value):
        if value < 0 or value >= self.n :
            raise IndexError

        return "this is a silly element "

s1 = Silly(10)

result = s1[0]    #returns  you are requesting item at 0
                   #this is a silly element

from functools import lru_cache 

@lru_cache(2**10)
def fib(n):
    return 1 if n < 2 else fib(n-1) + fib(n-2) 

result = fib(5)

class Fib:

    def __init__(self, n ):
        self.n = n 

    def __len__(self):
        return self.n 

    def __getitem__(self, s): #Assuming, s could be an index or slice
        if isinstance(s, int):
            if s < 0 :  # transforming negative index to positive, but if will still raise an index error if the value after transformation is not within the bounds.
                s = self.n + s

            if s < 0 or s>= self.n:
                raise IndexError

            return Fib._fib(s)
        else:
            start, stop, step = s.indices(self.n)
            rnge = list(range(start, stop, step))
            return [Fib._fib(n) for n in rnge]
            

    @staticmethod
    @lru_cache(2**10)
    def _fib(n):
        return 1 if n < 2 else Fib._fib(n-1) + Fib._fib(n-2)      

f = Fib(8)

#positive index 
result = f[6]     #return 13
#negative index
result = f[-1]    #return 21 , f[-1] is equivalent to f[7]

#iteration
result = list(f)  #return [1, 1, 2, 3, 5, 8, 13, 21]
result = [item**2 for item in f] #return [1, 1, 4, 9, 25, 64, 169, 441]

#slicing
result = f[:5]    #return [1, 1, 2, 3, 5]

#negative index slicing
result = f[-1: -4: -1] #return [21, 13, 8]


"""In place concatenation and repeatation"""

l1 = [1,2,3,4]
l2 = [5,6]

result = id(l1) #returns 2766816092424
result = id(l2) #returns 2766810635080

l1 = l1+l2 
result = id(l1) #returns 2766816206984
#all the three memory addresses are different 

#but let's say if we use +=, then it's not same as above. It's a inplace mutation.(works with any iterble)
l1 = [1,2,3,4]
l2 = [5,6]

result = id(l1) #returns 2766816092424
result = id(l2) #returns 2766810635080

l1 += l2
result = id(l1) #returns 2124207759624

"""combining list and tuples
--> If we try to use "+" operator to do so, it will not work.(throw an error), but instead we can use the "+=" operator to conmcatenate a list and a tuple
""" 
l1 = [1,2,3,4]
t1 = (5,6)

result = id(l1) #returns 2463992896456

l1+=t1 # l1 = [1, 2, 3, 4, 5, 6]
result = id(l1) #returns 2463992896456

#i.e the id of list has not changed, i.e it was a inplace mutation. we can do inplace mutations for mutable iterables only. for example:
l1 += range(7,10) # l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]

#the same concept is true for "*=" operator as well 

l1 = [7,6,5]

result = id(l1) # return 2449351909576

l1 *= 2 # [7, 6, 5, 7, 6, 5]
result = id(l1) # return 2449351909576

"""part 2: Custom sequences: Introducing mutability"""

#example to show that we can over write the addition and in place addition properties of a sequence type as per the wish 

class Myclass:

    def __init__(self, name):
        self.name = name 

    def __repr__(self):
        return "my class name is {}".format(self.name)
    
    def __add__(self, other):
        return "Hello from __add___"

    def __idd__(self, other):
        print('You called += on {self} and {other}')
        return "Hello from __iadd___"

c1 = Myclass("instance1")
c2 = Myclass("instance2")

result = c1 + c2 # return "Hello from __add___"

#let's redo it the way it is usally expected to do 
class Myclass:

    def __init__(self, name):
        self.name = name 

    def __repr__(self):
        return f'Myclass(name = {self.name})'
    
    def __add__(self, other):
        return Myclass(self.name + other.name)

    def __iadd__(self, other):
        if isinstance(other, Myclass):
            self.name += other.name
        else:
            self.name += other

        return self
    
    def __mul__(self, n):
        if isinstance(n , int):
            return Myclass(self.name * n)
        else:
            raise TypeError(f'Unsupported operand type {type(n)} and {type(self)}')

    def __rmul__(self, n): # right multiplication -- > can be used if someone calls n * Myclass(name), so python will implement the right_multiply method. 
        if isinstance(n , int):
            return Myclass(self.name * n)

    def __imul__(self, n):
        if isinstance(n , int):
            self.name *= n
        
        return self
    
    def __contains__(self, value):
        return value in self.name

#normal concatenation
c1 = Myclass("Pulkit")
c2 = Myclass("Aanisha")

id(c1) #1683600485008
id(c2) #1683600484840

result = c1+c2 
result, id(result) # Myclass(name = PulkitAanisha) 1683600484896

#inplace concatenation 
c1 += c2
c1, id(c1) # Myclass(name = PulkitAanisha), 1683600485008 --> the id is still same

#normal multiplication
c3 = Myclass("Gauri")
id(c3) # 139283509950

result = c3*3  
result, id(result) # Myclass(name = GauriGauriGauri) 1972831779752

#inplace multiplication
c4 = Myclass("abcd")
id(c4)  # 2135593380720)

c4 *= 3
c4, id(c4)  #Myclass(name = abcdabcdabcd) 2135593380720 -- >Id is same

#right multiplication 
c1 = Myclass("qwerty")

c1 * 3  # returns Myclass(name = qwertyqwertyqwerty)
3 * c1  # returns Myclass(name = qwertyqwertyqwerty)

#checking containment 
result = "qwe" in c1    #return True
result = "z" in c1      #return False


#Example 2: Custom Sequence
import numbers 

class Point:
    def __init__(self, x, y ):
        if isinstance(x, numbers.Real) and isinstance(x, numbers.Real):
            self._pt = (x, y)
        else:
            raise TypeError("Point co-ordinates must be real numbers")

    def __repr__(self):
        return f'Point(x = {self._pt[0]}, y = {self._pt[1]})'

    def __len__(self):
        return len(self._pt)

    def __getitem__(self, s):
        return self._pt[s]
    
p1 = Point(10, 20)

#unpacking the points from the Point class
x, y = p1 # 10, 20

#this is helpful in cases when we want to use the existing point to create another point
p2 = Point(*p1)
p2 # Point(x = 10, y = 20)

class Polygon:

    def __init__(self, *pts):

        if pts: 
            self. _pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []

    def __repr__(self):

        pts_str = ", ".join([str(pt) for pt in self._pts]) # if we don't do this the and directly pass the self._pts, the representation would look like this - > Polygon([Point(x = 0, y = 0), Point(x = 10, y = 20)])
        return f"Polygon({pts_str})"

    def __len__(self):
        return len(self._pts)

    def __getitem__(self, s): # since we are pasing tuples,w e can let tuples handle slicing, indexing ...
        return self._pts[s]

    def __setitem__(self, s, value):

        try:
            rhs = [Point(*pt) for pt in value]
            is_single = False
        except TypeError:
            try:
                rhs = Point(*value)
                is_single = True
            except TypeError:
                raise TypeError("Invalid Point or iterable of Points")
        
        if isinstance(s, int) and is_single:
            self.insert(s, rhs)
        elif isinstance(s, slice) and not is_single:
            self._pts[s] = rhs
        else:
            raise TypeError("Incompatible Index/Slice assignment")

    def __add__(self, other):
        if isinstance(other, Polygon):
            new_pts = self._pts + other._pts
            return Polygon(*new_pts)
        else:
            raise TypeError("can only concatenate with another Polygon")

    def __iadd__(self, other):
        if isinstance(other, Polygon):
            points = other._pts
        else:
            points = [Point(*pt) for pt in other]

        self._pts = self._pts + points
        return self
    
    def append(self, pt):
        self._pts.append(Point(*pt)) 

    def insert(self, i , pt):
        self._pts.insert(i, Point(*pt) )

    def extend(self, others):
        if isinstance(others, Polygon):
            self._pts += others._pts
        else:
            points = [Point(*pt) for pt in others]
            self._pts += points

    def __delitem__(self, s):
        del self._pts[s]
    
    def pop(self, i):
        return self._pts.pop(i)

p1 = Polygon((0, 0), (1, 1))

p1      # Polygon(Point(x = 0, y = 0), Point(x = 1, y = 1))
len(p1) # 2

#indexing and slicing
p1[0]    # Point(x = 0, y = 0)
p1[0:2]  # [Point(x = 0, y = 0), Point(x = 1, y = 1)]

# Normal addition/concatenation
p1 = Polygon((0, 0), (1, 1))
p2 = Polygon((2, 2), (3, 3))
result = p1 + p2 #return Polygon(Point(x = 0, y = 0), Point(x = 1, y = 1), Point(x = 2, y = 2), Point(x = 3, y = 3))

#Inplace concatenation 
p1 = Polygon((0, 0), (1, 1))
p2 = Polygon((4, 4), (5, 5))
p1 += p2 #return [Point(x = 0, y = 0), Point(x = 1, y = 1), Point(x = 4, y = 4), Point(x = 5, y = 5)]

#inplace concatenation with any iterables, not just Polygons
p1 = Polygon((0, 0), (1, 1))
p2 = [(2,2), (3,3)]
p1+=p2 # return Polygon(Point(x = 0, y = 0), Point(x = 1, y = 1), Point(x = 2, y = 2), Point(x = 3, y = 3))

#append
p1 = Polygon((0, 0), (1, 1))
p1.append([10,10]) #Polygon(Point(x = 0, y = 0), Point(x = 1, y = 1), Point(x = 10, y = 10))

#Insertion
p1 = Polygon((0, 0), (1, 1))
p1.insert(1, Point(-1, -1)) # Polygon(Point(x = 0, y = 0), Point(x = -1, y = -1), Point(x = 1, y = 1))

#Extend
p1 = Polygon((0, 0), (1, 1))
p2 = Polygon((2,3), (4,5))  #Polygon(Point(x = 0, y = 0), Point(x = 1, y = 1), Point(x = 2, y = 3), Point(x = 4, y = 5))
p1.extend(p2)

#extend, example 2:
p1 = Polygon((0, 0), (1, 1))
p1.extend([(0,0), Point(20,20)]) # return Polygon(Point(x = 0, y = 0), Point(x = 1, y = 1), Point(x = 0, y = 0), Point(x = 20, y = 20))

#Inplace slicing
p1 = Polygon((0, 0), (1, 1))
p1[0:1] = [(3,4), Point(10, 20), [30,30]] 
p1  #retun Polygon(Point(x = 3, y = 4), Point(x = 10, y = 20), Point(x = 30, y = 30), Point(x = 1, y = 1)) 

#another way of insertion
p1 = Polygon((0, 0), (1, 1))
p1[0] = (9,9) 
p1 # return Polygon(Point(x = 9, y = 9), Point(x = 0, y = 0), Point(x = 1, y = 1))

#deletion using slicing or index
p = Polygon((0,0), (1,1), (2,2), (3,3))

del p[0]  #p == Polygon(Point(x = 1, y = 1), Point(x = 2, y = 2), Point(x = 3, y = 3))

del p[0:2] # p = Polygon(Point(x = 3, y = 3))

#pop 
p = Polygon((0,0), (1,1), (2,2), (3,3))
p.pop(2) #return Polygon(Point(x = 0, y = 0), Point(x = 1, y = 1), Point(x = 3, y = 3))




print(p)