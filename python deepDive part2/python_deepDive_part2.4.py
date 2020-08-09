# python_deepDive part 2, Module 4
# python version: 3.7.3

"""
This module contains the following:
    1. Combinatorics in itertools module--> product, permutations, combinations, combinations_with_replacement
    2. Context managers: A state surrounding a section of code
    3. Generators and context managers: Creating a context manager from generator fucntions. 
    4. Decorating Generator functions
Definitions: 
Predicate: A function which takes a single argument and returns True or False
"""

"""Combinatorics--> product"""
import itertools

def matrix(n):
    for i in range(1, n+1):
        for j in range(1, n+1):
            yield f'{i} * {j} = {i*j}'

result = list(itertools.islice(matrix(10), 10, 20))

l1 = ["x1", "x2", "x3", "x4"]
l2 = ["y1", "y2", "y3"]

def myfunc(l1, l2):
    for x in l1:
        for y in l2:
            yield (x, y)

result = list(myfunc(l1, l2))  # returns [('x1', 'y1'), ('x1', 'y2'), ('x1', 'y3'), ('x2', 'y1'), ('x2', 'y2'), ('x2', 'y3'), ('x3', 'y1'), ('x3', 'y2'), ('x3', 'y3'), ('x4', 'y1'), ('x4', 'y2'), ('x4', 'y3')]

# instead of this we can use itertools cartesian product function, which returns a laxy iterator
result = list(itertools.product(l1, l2)) #returns [('x1', 'y1'), ('x1', 'y2'), ('x1', 'y3'), ('x2', 'y1'), ('x2', 'y2'), ('x2', 'y3'), ('x3', 'y1'), ('x3', 'y2'), ('x3', 'y3'), ('x4', 'y1'), ('x4', 'y2'), ('x4', 'y3')]

"""Combinatorics--> permutations, combinations"""
l1 = "abc"
result = list(itertools.permutations(l1))  #[('a', 'b', 'c'), ('a', 'c', 'b'), ('b', 'a', 'c'), ('b', 'c', 'a'), ('c', 'a', 'b'), ('c', 'b', 'a')] 

#we can pass an optional parameter to define the length of the permutations
result = list(itertools.permutations(l1, 2))  #[('a', 'b'), ('a', 'c'), ('b', 'a'), ('b', 'c'), ('c', 'a'), ('c', 'b')]

#combinations: the order doesn't matter unlike permutations.
result = list(itertools.combinations([1,2,3,4], 2)) #returns [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]

# we can run it with replacemnets as well
result = list(itertools.combinations_with_replacement([1,2,3,4], 2)) #returns [(1, 1), (1, 2), (1, 3), (1, 4), (2, 2), (2, 3), (2, 4), (3, 3), (3, 4), (4, 4)]

"""
Context Managers
Context Manager protocols: 
__enter__()
__exit__()  --> can choose to handle the exception-- > silence or propogate it
"""

with open("test.text", "w") as f:
    is_file_closed = f.closed #returns False

is_file_closed = f.closed  # returns True

#Console Logs:
"""
Custom Context Manager
key points:
1. Doesn't have it's own local scope.
2. The "with" statement is what causes us to enter the context. 
"""

#Example 1:
class MyContext:

    def __init__(self):
        self.obj  = None

    def __enter__(self):
        print("entering context..")
        self.obj = "the return object"
        return self.obj
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        print("exiting context")
        if exc_type:
            print(f'*** Error Occured : {exc_type}, {exc_value}')

        return False
        """return False if you want to propogate the exception or True to silence it if it occurs."""

# with MyContext() as obj:
#     print("Inside with block", obj)
#     raise ValueError("custom message")

#Console Logs:
"""
The tricky part to keep in mind here is that the obj is not the instance of Mycontext but instead it is ==> obj = Mycontext().__enter__() and 
The __exit__ part will always run , no matter what. 

entering context..
Inside with block the return object
exiting context
*** Error Occured : <class 'ValueError'>, custom message
Traceback (most recent call last):
  File "python_deepDive_part2.4.py", line 83, in <module>
    raise ValueError("custom message")
ValueError: custom message

"""
#we can supress the exception by returning True in the __exit__ block
class MyContext:

    def __init__(self):
        self.obj  = None

    def __enter__(self):
        print("entering context..")
        self.obj = "the return object"
        return self.obj
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        print("exiting context")
        if exc_type:
            print(f'*** Error Occured : {exc_type}, {exc_value}')
        return True #supresses the exception

with MyContext() as obj:
    print("Inside with block", obj)
    raise ValueError("custom message")

#Console Logs:
"""
entering context..
Inside with block the return object
exiting context
*** Error Occured : <class 'ValueError'>, custom message
"""
#Example 2: 
class Resource:
    def __init__(self, name):
        self.name = name 
        self.state = None 

class ResourceManager:
    def __init__(self, name):
        self.name = name
        self.resource = None 
    
    def __enter__(self):
        print("entering context")
        self.resource = Resource(self.name)
        self.resource.state = "created"
        return self.resource
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        print("exiting context")
        self.resource.state =  "destroyed"
        if exc_type:
            print("error occured")
        return False

with ResourceManager("spam") as res:
    print(f'{res.name} = {res.state}')
print(f'{res.name} = {res.state}')

#Console Logs:
"""
entering context
spam = created
exiting context
spam = destroyed
"""
#the res object is in our global scope, we can check it using: 
result = 'res' in globals()  #returns True

#Application 1:
class File:
    def __init__(self, name , mode):
        self.name = name 
        self.mode = mode 
    
    def __enter__(self):
        print("opening file")
        self.file = open(self.name, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        print("closing file")
        self.file.close()
        return False

with File("test.text", "w") as f:
    f.write("This is a test sentence")

#Console Logs:
"""
opening file
closing file
"""

with File("test.text", "r") as f:
    print(f.readlines())

#console log:
"""
opening file
['This is a test sentence']
closing file
"""

#Application 2:
import decimal 

#decimal has a context manager
decimal.getcontext() #returns Context(prec=28, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999, capitals=1, clamp=0, flags=[], traps=[InvalidOperation, DivisionByZero, Overflow])
#and, if we change the context, it gets changed globally, but let's say we want to temporarily change the context then the context managers would be very useful. 

#Adhoc way 
old_prec = decimal.getcontext().prec

decimal.getcontext().prec = 4
decimal.Decimal(1)/decimal.Decimal(3) #returns 0.3333
decimal.getcontext().prec = old_prec

decimal.Decimal(1)/decimal.Decimal(3) #returns 0.3333333333333333333333333333

#Context manager for changing precision
class precision:
    def __init__(self, prec):
        self.prec = prec
        self.current_prec = decimal.getcontext().prec

    def __enter__(self):
        decimal.getcontext().prec = self.prec

    def __exit__(self, exc_type, exc_value, exc_tb):
        decimal.getcontext().prec = self.current_prec
        return False

with precision(3):
    decimal.Decimal(1)/decimal.Decimal(3) #returns 0.3333
decimal.Decimal(1)/decimal.Decimal(3)  #returns 0.3333333333333333333333333333


#since doing this in decimal class is very common it has it's own context manager which is very generic and can be used as shown below:
with decimal.localcontext() as ctx:
    ctx.prec = 3
    decimal.Decimal(1)/decimal.Decimal(3) #returns 0.3333
decimal.Decimal(1)/decimal.Decimal(3)

#Application 3: timing the implementation of a code block
from time import perf_counter, sleep

class Timer:
    def __init__(self):
        self.elapsed = 0 

    def __enter__(self):
        self.start = perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.stop = perf_counter()
        self.elapsed = self.stop - self.start 
        return False 

with Timer() as timer:
    sleep(1)

timer.elapsed  #returns 1.0000387

#Application 4: Changing the standardOutput(stdout) location when we use a print statement using the sys module
import sys 

class OutToFile:
    def __init__(self, fname):
        self._fname = fname 
        self._current_stdout = sys.stdout
    
    def __enter__(self):
        self._file = open(self._fname, "w")
        sys.stdout = self._file 
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        sys.stdout = self._current_stdout
        self._file.close()
        return False

#as alias is not necessary here because__enter__ is not returning anything. 
with OutToFile("test.text"):
    print("Line 1")
    print("Line 2")
    print("Line 3")
    print(sys.stdout)  #<_io.TextIOWrapper name='test.text' mode='w' encoding='cp1252'>

sys.stdout #<_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
#the print statments will not get printed to the console but instead added to the file "test.txt", we can check this: 

with open("test.text", "r") as f:
    lines = f.readlines()  #returns ['Line 1\n', 'Line 2\n', 'Line 3\n', "<_io.TextIOWrapper name='test.text' mode='w' encoding='cp1252'>\n"]

#Application 5: Opening and closing HTML tags 
class Tag:
    def __init__(self, tag):
        self._tag  = tag

    def __enter__(self):
        print(f'<{self._tag}>', end = " ")
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        print(f'</{self._tag}>', end = " ")


with Tag("p"): 
    print("some", end = " ")

    with Tag("b"):
        print("bold", end = " ")

    print("text", end = " ")

#console Log: <p> some <b> bold </b> text </p>

#Application 6: Context manager where we can call the __enter__ and __exit__ method multiple times
"""
Structure:

Title
    - Item 1 
      -   Sub item 1a
      -   Sub item 1b
    - Item 2 
      -   Sub itme 2a 
      -   Sub itme 2b 
"""

class ListMaker:

    def __init__(self, title, prefix = "- ", indent = 3):
        self._title = title 
        self._prefix = prefix 
        self._indent = indent 
        self._current_indent = 0 
        print(title)

    def __enter__(self):
        #adding indentation while entering
        self._current_indent += self._indent
        return self #so that we can re-enter the instance of ListMaker and keep a track of what has happened before. 
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        #removing indentation with exiting
        self._current_indent -= self._indent
        return False
    
    def print_item(self, arg):
        print(" " * self._current_indent + self._prefix + str(arg))

with ListMaker("Items") as lm:
    lm.print_item("Item 1")
    with lm:
        lm.print_item("Sub item 1a")
        lm.print_item("Sub item 1b")

    lm.print_item("Item 2")
    with lm:
        lm.print_item("Sub item 2a")
        lm.print_item("Sub item 2b")

#console Log:
"""
   - Item 1
      - Sub item 1a
      - Sub item 1b
   - Item 2
      - Sub item 2a
      - Sub item 2b
"""

#To output our content to a file:
with OutToFile("test.text"):
    with ListMaker("Items") as lm:
        lm.print_item("Item 1")
        with lm:
            lm.print_item("Sub item 1a")
            lm.print_item("Sub item 1b")

        lm.print_item("Item 2")
        with lm:
            lm.print_item("Sub item 2a")
            lm.print_item("Sub item 2b")


"""Generators and context managers"""

def my_gen():
    try:
        print("creating context and yielding object")
        yield [1,2,3,4]
    finally:
        print("exiting context and cleaning up")

gen = my_gen()
lst = next(gen)
print(lst)
try:
    next(gen)
except StopIteration:
    pass

#console Log:
"""
creating context and yielding object
[1, 2, 3, 4]
exiting context and cleaning up
"""
#Instead this we can build a generic generator context manager class which will do this for us:
class GeneratorContextManager:
    def __init__(self, gen_func, *args, **kwargs):
        self._gen = gen_func(*args, **kwargs)

    def __enter__(self):
        return next(self._gen)

    def __exit__(self, exc_type, exc_value, exc_tb):
        try: 
            next(self._gen)
        except StopIteration:
            pass

        return False 

with GeneratorContextManager(my_gen) as gen:
    print("Inside context manager")
    print(gen)

#Console Log:
"""
creating context and yielding object
Inside context manager
[1, 2, 3, 4]
exiting context and cleaning up
"""

#let's try to build a file manager generator and use it with context manager.
def open_file(fname, mode):
    f = open(fname, mode)
    try:
        print("opening file...")
        yield f 
    finally:
        print("closing file....")
        f.close()

with GeneratorContextManager(open_file, 'test.text', "w") as f:
    f.writelines("testing...")

#console log:
"""
opening file...
closing file....
"""

with GeneratorContextManager(open_file, 'test.text', "r") as f:
    print(f.readlines())

#console log
"""
opening file...
['testing...']
closing file....
"""

"""Decorating generator functions"""

