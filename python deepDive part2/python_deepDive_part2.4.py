# python_deepDive part 2, Module 4
# python version: 3.7.3

"""
This module contains the following:
    1. Combinatorics in itertools module--> product, permutations, combinations, combinations_with_replacement
    2. Context managers: A state surrounding a section of code
    3. Generators and context managers: Creating a context manager from generator fucntions. 
    4. Decorating Generator functions with context managers
    5. Generators and co-routines
        a. Generator State
        b. Sending to Generators
        3. closing generators

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
    sleep(0.01)  # TODO

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

"""Decorating generator functions with context managers"""
class GeneratorContextManager:
    def __init__(self, gen_obj):
        self._gen = gen_obj

    def __enter__(self):
        print("calling next to get the yielded value from the generator")
        return next(self._gen)

    def __exit__(self, exc_type, exc_value, exc_tb):
        print("calling next to perform cleanup in generator")
        try: 
            next(self._gen)
        except StopIteration:
            pass

        return False 

def contextManager_decorator(gen_func):
    def helper(*args , **kwargs):
        gen = gen_func(*args, **kwargs)
        return GeneratorContextManager(gen)
    return helper

@contextManager_decorator
def open_file(fname, mode = 'r'):  #equivalent to --> open_file = contextManager_decorator(open_file)

    print("opening file...")
    f = open(fname, mode)
    try:
        yield f 
    finally:
        print("closing file")
        f.close()

with open_file("test.text", "w") as f:
    f.writelines("writing.....")

#console log :
"""
calling next to get the yielded value from the generator
opening file...
calling next to perform cleanup in generator
closing file
"""
with open_file("test.text", "r") as f:
    print(f.readlines())

#console log:
"""
calling next to get the yielded value from the generator
opening file...
['writing.....']
calling next to perform cleanup in generator
closing file
"""

#there is an inbuild context manager decorator in contextlib module, it has better inbuilt exception handling codes hance preferred
from contextlib import contextmanager  

@contextmanager
def open_file(fname, mode = 'r'):

    print("opening file...")
    f = open(fname, mode)
    try:
        yield f 
    finally:
        print("closing file...")
        f.close()

with open_file("test.text", "w") as f:
    f.writelines("writing.....")

#console log :
"""
opening file...
closing file...
"""
with open_file("test.text", "r") as f:
    print(f.readlines())

#console log:
"""
opening file...
['writing.....']
closing file...
"""
#Example 2: Timing an execution

@contextmanager
def timer():
    stats = dict()
    start = perf_counter()
    stats["start"] = start 

    try:
        yield stats 
    finally:
        stop = perf_counter()
        stats["stop"] = stop
        stats["elapsed"] = stop - start 

with timer() as stats:
    sleep(0.01)  #TODO

stats  # return {'start': 1.1521731, 'stop': 2.1524884, 'elapsed': 1.0003153000000002}

#example 3 : redirecting the stdout location

import sys 
@contextmanager
def out_to_file(fname):
    current_stdout = sys.stdout 
    file = open(fname, "w")
    sys.stdout = file 
    try:
        yield
    finally:
        file.close()
        sys.stdout = current_stdout 

with out_to_file("test.text"):
    print("Test statement 1", end = " ")
    print("Test statement 2", end = " ")

with open_file("test.text", "r") as f:
    print(f.readlines())

#console log:
"""
opening file...
['Test statement 1 Test statement 2 ']
closing file...
"""

#redirecting output is so common that python has an inbuilt context manager for that, but it doesn't accept a file name, but instead it takes file_object as an input
from contextlib import redirect_stdout

#Method 1 
f = open("test.text", 'w')
with redirect_stdout(f):
        print("new log data...")
f.close()

with open_file("test.text", "r") as f:
    print(f.readlines())    #returns ['new log data...\n']

#Method 2 : use conetxt managers
with open("test.text", "w") as f:
    with redirect_stdout(f):
        print("new log data...")

with open_file("test.text", "r") as f:
    f.readlines()    #returns ['new log data...\n']


"""
------------------------------
Generators and coroutines
------------------------------
--> coroutines are actually co-operative routines(functions), which are coordinating between two events. 

Extras:
Abstract Data structures

Stack: Last in first out
    Sample Implementation :
        stack = []
        stack.append(element)
        stack.pop()

Queue : First in First out
    Sample Implementation :
        queue = []
        queue.insert(0, element)
        queue.pop()

In case of Queue, the insertion process at index 0 is highly inefficient, hence w ecan use deque from the collections module. 
"""

print("---------------------------\n\n")

from collections import deque

dq = deque([1,2,3,4,5])

#appending an element on the right side 
dq.append(100)  
dq  #returns deque([1, 2, 3, 4, 5, 100])

#appending an element on the left side
dq.appendleft(-10) 
dq  #returns deque([-10, 1, 2, 3, 4, 5, 100])

#removing the last element from the deque
dq.pop()  #returns 100
dq  #returns deque([-10, 1, 2, 3, 4, 5])

#removing the first element from the deque 
dq.popleft()  #returns -10
dq  #returns deque([1, 2, 3, 4, 5])

#deque has a maxlen property, which maintains the max length of the list and removes elements as shown below:
dq = deque([1,2,3,4], maxlen = 5)
len(dq) #returns 4
dq.maxlen #returns 5

dq.append(100)  
dq #returns deque([1, 2, 3, 4, 100], maxlen=5)

#Let's try to add a new element from the left
dq.appendleft(0)
dq  #returns deque([0, 1, 2, 3, 4], maxlen=5) -- > removed the right most element from the list

#let's try to add an elemet from right again 
dq.append(20)
dq  #returns deque([1, 2, 3, 4, 20], maxlen=5)

#Example 1: Building a producer, consumer and a co-ordinator of values.

#producing sample elements
def produce_elements(dq):
    for i in range(1, 6):
        dq.appendleft(i)

#consuming elements produced by the producer
def consume_elements(dq):
    while len(dq) >0:
        item = dq.pop()
        print("processing item: ", item)

#coordinating the events
def coordinator():
    dq = deque()
    produce_elements(dq)
    consume_elements(dq)

coordinator()
#console log:
"""
processing item:  1
processing item:  2
processing item:  3
processing item:  4
processing item:  5
"""

# let's say there are huge number of elements which the producer is producing, and hence we need to consume them as  batch processs as handling them at once would be 
# too much consumption of memory and time.

#producing sample elements but with an added condition to limit the number of elements at a time
def produce_elements(dq, n):
    for i in range(1, n):
        dq.appendleft(i)
        if len(dq) == dq.maxlen:  #this means that the queue is full
            print("Queue Filled")
            yield  #using the yield to give control to the consumer, and not to yield any value

#consuming elements produced by the producer
def consume_elements(dq):
    while True:
        while len(dq) > 0:
            item = dq.pop()
            print("processing item: ", item)
        print("Queue empty - yielding control")
        yield #again we are using yield to give the control back to the producer

#coordinating the events
def coordinator(max_length):

    dq = deque(maxlen = max_length)
    producer = produce_elements(dq, 100)
    consumer = consume_elements(dq)

    while True:
        try:
            print("producing...")
            next(producer)
        except StopIteration:
            print("producer is finished...")
            break
        finally:
            print("consuming...")
            next(consumer)

coordinator(20)

"""
---------------------
Generator States
---------------------
def my_gen(fname):
    f = open(f_name)
    try:
        for row in f:
            yield row
    finally:
        f.close()

4 states:
    g = my_gen()  --> gen_creatd
    row = next(g) --> gen_suspended 
    lst(g)--> claling next until the generator is done --> gen_closed
    inside the generator code --> gen_running
"""
from inspect import getgeneratorstate

def gen(s):
    for c in s:
        yield c

g = gen("abc")
getgeneratorstate(g) #returns GEN_CREATED
next(g) #returns "a"
getgeneratorstate(g) # returns GEN_SUSPENDED
list(g)  # genertaes rest of the characters -> ["b", "c"]
getgeneratorstate(g) #returns GEN_CLOSED

#in order to get the generator running state, we need to make an assumption about the instance of the function object which will get created in the global space
def gen(s):
    for c in s:
        print(getgeneratorstate(global_gen)) # since this variable is not defined in the local scope, python is going to look for it in the global scope.
        yield c

global_gen = gen("abc")
next(global_gen) # returns "a", console log: GEN_RUNNING
getgeneratorstate(g) # returns GEN_SUSPENDED

"""
--------------------------
Sending to generators
--------------------------
key points:
1. yield when used like --> <var> = yield <var2- optional> works like an expression.
2. In order to be able to send the data the generator function must be in suspended state. The generator is suspended right before "|yield"--> the pipe shows the locations where the generator gets suspended. 
3. if the generator yields a finite value, then it will give an stopiteration error once it has been yielded that many times. 
"""
print("---------------------------\n\n")

def echo():
    while True:
        received = yield 
        print("you said:", received )

e = echo()

from inspect import getgeneratorstate
getgeneratorstate(e) #returns GEN_CREATED
#we cannot send any data right now, the generator is currently in created mode, we need ot bring in it to the suspended more before we can send something to it.

next(e) #this process of bringing a generator from creation state to suspended state is called as priming
getgeneratorstate(e) #returns GEN_SUSPENDED

e.send("python") #console log: you said: python
e.send("hello") #console log: you said: hello

#we can send a value to any genertor object, for example
def squares(n):
    for i  in range(n):
        yield i**2

sq = squares(5) # creation mode
#bring it to suspended mode
next(sq) #returns 0
sq.send("hello world") # returns 1 : because we didn't assign it to anything it was just discarded

#way to bring a generator to it's suspended state from creation state
def echo():
    while True:
        received = yield 
        print("you said:", received )

e = echo()
#we are allowed to send a None object to just created generator, if we try to send anything else it will throw an error.
e.send(None)
getgeneratorstate(e)  #returns GEN_SUSPENDED
e.send("hello world")  #console log : you said: hello world

#we can even modify the square obejct to do both, reveice values and yield squares
def squares(n):
    for i  in range(n):
        received = yield i**2
        print("received:", received)

sq = squares(5) # creation mode
#bring it to suspended mode
next(sq) #returns 0
sq.send("python") 

#console Log:
"""
----------------------------
received: python 
1
-----------------------------
Key points:
1. Notice here that generator was in a suspended state, it first received the value, moved to the next line to print "received: python " and 
then continued the loop and yielded 1.

2. It's important to understand that the generator is suspended right before "|yield"--> the pipe shows the locations where the generator gets suspended. 
"""

#the generator will throw a stopIteration error once it has exhausted the loop, for example:
def echo(max_len):
    for _ in range(max_len):
        received = yield
        print("you said:", received)
    print("that's all")

e = echo(3)
next(e)
e.send("python")
e.send("is")
# e.send("awesome") #uncomment to see the stopiteration error

#Console Log:
"""
you said: python
you said: is
you said: awesome
that's all
Traceback (most recent call last):
  File "python_deepDive_part2.4.py", line 884, in <module>
    e.send("awesome")
StopIteration
"""

#Application 1: running averages 
def running_averager():
    total = 0 
    count = 0 
    average = None
    while True:
        received = yield average
        total += received
        count +=1
        average = total/count

def running_averages(iterable):
    averager = running_averager()
    next(averager)
    for value in iterable:
        running_average = averager.send(value)
        print(running_average)

running_averages((1,2,3,4))  #returns 1.0, 1.5, 2.0, 2.5


"""
--------------------
Closing generators
--------------------
"""

from inspect import getgeneratorstate

import csv 

def parse_file(f_name):
    print("opening file..")
    f = open(f_name, "r")
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        reader = csv.reader(f, dialect = dialect)
        for row in reader:
            yield row 
    finally:
        print("closing file...")
        f.close()

import itertools

parser = parse_file("../Training Datasets/cars.csv")

for row in itertools.islice(parser, 10):
    print(row)

#now let's say we only want to run these 10 lines and close the file, we can do this by:
parser.close() #console log: "closing file..."
#here is how it happened to see what is happening

def parse_file(f_name):
    print("opening file..")
    f = open(f_name, "r")
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        reader = csv.reader(f, dialect = dialect)
        for row in reader:
            yield row 
    except Exception as e:
        print("some exception occured", str(e))
    except GeneratorExit:
        print("Generator was closed")
    finally:
        print("closing file...")
        f.close()

parser = parse_file("../Training Datasets/cars.csv")

for row in itertools.islice(parser, 10):
    print(row)

parser.close()
#console log:
"""
-----------------
Generator was closed
closing file...
------------------
key points:
1. GeneratorExit is not a child class of Exception, so the exception isn't going to catch it.
2. when we call the generator.close(), it raise the GeneratorExit exception insidee the generator. Hence it first prints the "generator was closed" and then finally part ran.
3. We cannot ignore the GeneratorExit exception and continue running our code wew will  get an error.

"""
#trying to catch the exception and continue running the generator :
def parse_file(f_name):
    print("opening file..")
    f = open(f_name, "r")
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        reader = csv.reader(f, dialect = dialect)
        for row in reader:
            try:
                yield row 
            except GeneratorExit:
                print("Ignore the exception and continue running")
    finally:
        print("closing file...")
        f.close()

parser = parse_file("../Training Datasets/cars.csv")

for row in itertools.islice(parser, 10):
    print(row)

# parser.close()# uncomment to see the below given error message
"""
Traceback (most recent call last):
  File "python_deepDive_part2.4.py", line 1014, in <module>
    parser.close()
RuntimeError: generator ignored GeneratorExit
Ignore the exception and continue running
"""