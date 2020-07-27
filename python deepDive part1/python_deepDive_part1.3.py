"""
This module covers the following:
    1.Scopes --> Local, Global, nonlocal, Nested
    2. Closures  **very very important concept 
    3. Decorators 
    4. building single_dispatch functions
"""

# Global and Local scopes
a = 10

def my_func(n): 
      c= n ** 2
      return c 

"""
Note: A variable is not local until it has been assigned inside the local scope, Here "c" and "n" both are under local scope,
whereas "a" is still under global scope. A global scope is accessible everywhere in the module, even under local scope as well. 

Python first tries to find something in the local scope, if it does not find it, it looks for it in Global scope and then finally looks in the Built-in scope,
if it doesn't find it there as well. Then it throws a run time error. 
"""
a = 10

def my_func(n):
    c = a ** n
    return c 

my_func(2) # returns 100, even though a has not been assigned inside the function. 

def my_func(n):
    a = 20 
    c = a ** n
    return c

my_func(2) # returns 400
a # returns 10, because the local scope cannot modify the global scope until speciifed. 

def my_func(n):
    global a 
    a = 20 
    c = a ** n
    return c

my_func(2) # returns 400 
a # returns 20, because we have specified it to be global. 

# let's take another function 
def my_func2():
    c = a**n 
    a = 100 
    return a

""" my_func2()  --> This will throw a "UnboundLocalError: local variable 'a' referenced before assignment" error because when the myfunc2 was created, 
python assigned "a" under local scope, because it has been assigned to a value of 100 later, so when we call the function it gives this error. 

Note: the variable becomes a local scope if it has been asssigned anywhere in the local scope, no matter where. 

"""

#Non-local scopes 

def outer_func():
    a = 10
    def inner_func():
        return a

    inner_func()

outer_func() # return 10 

"""
Now here, There are 4 scopes --> inner_func scope, outer_func scope, global scope and Built-in scope, 
So when we call the outer_func, the inner_func looks tries to find "a" within it's local scope and when it doesn't find it, it looks for 
scope under outer_func, this scope is called as nonlocal scope, because it's neither Local nor Global 
"""

def outer_func():
    x = "hello"

    def inner_func():
        x = "python"
    
    inner_func()
    
    return x 

outer_func() # returns "hello"

#we can however modify,nonlocal variables : It will however not look into GLobaL scope 

#case 1
def outer_func():
    x = "hello"

    def inner_func():
        nonlocal x
        x = "python"
    
    inner_func()
    
    return x 

a = outer_func() # returns "Python"

"""
Whenever python is told that a variable is non local, it will look for it in the enclosing local space chain unitl it first encounters the specified variable name. 
BEWARE: It will only look in the local scopes, not global scopes. 
"""
#case 2 
def outer():
    x = "hello"

    def inner1():

        def inner2():
            nonlocal x 
            x = "Python"
            
        inner2()
    inner1()
    return x 

a = outer() # Returns "Python"

#case 3
def outer():
    x = "hello"

    def inner1():
        x = "python"
        def inner2():
            nonlocal x 
            x = "Pulkit"
        inner2()
    inner1()

    return x

a = outer() # returns "hello" because inner2() changed the value of x under inner1() and not the x under outer()

#case 4 
def outer():
    x = "Hello"

    def inner1():
        nonlocal x 
        x = "python"

        def inner2():
            nonlocal x 
            x = "pulkit"
        
        print("Inner(before): ", x)
        inner2()
        print("Inner(after):", x)
    
    inner1()
    return x 

"""a = outer()"""  # returns "pulkit" because the x inside inner1() referenced to the x under outer(), so when inner2() changed the value of x, the value of x gets changed for both 
#outer() and inner1()


"""CLOSURES"""

def outer():
    x = "python"

    def inner():
        print(x)

    return inner

fn = outer() 
"""
when we are returning the inner function here, we are not just returning the inner function but also the value associated with the free variable inside that function
and togther they are called as closures. We can see the list of free varibles and closure's --> cell address as well as the object memory address it is pointing to using 
the following: 
"""
fn.__code__.co_freevars # returns ('x',)
fn.__closure__ # returns (<cell at 0x000002874CD26288: str object at 0x000002874CE66260>,)


def outer():
    x = [1,2,3]
    # print("outer: ", hex(id(x)))

    def inner():
        y = x  # Note that the variable x is not assigned under inner function, it has just been referenced. So it will act as a free variable. 
        # print("inner: ", hex(id(y)))

    return inner 

lala = outer() 
lala()
#both will print same memory address, 

# Case: Single reference closures 
def outer():
    count = 0 

    def inc():
        nonlocal count
        count+=1 
        return count 
    return inc

fn = outer()

fn.__code__.co_freevars # retruns ('count',)
fn.__closure__   #returns (<cell at 0x0000013003B45FA8: int object at 0x00007FFD8C016270>,)

fn() # returns 1 
fn.__closure__ # return (<cell at 0x000001C2EAD45FA8: int object at 0x00007FFD8C016290>,)
# we will notice that the memory addresses has changed because the value of count has changed from 0 to 1

fn() # returns 2 
fn() # returns 3

#Case : single reference multi closures 
def outer():
    count = 0 

    def inc1():
        nonlocal count 
        count +=1 
        return count 
    
    def inc2():
        nonlocal count 
        count +=1 
        return count 

    return inc1, inc2

fn1, fn2 = outer()

fn1.__code__.co_freevars # returns ('count',)
fn2.__code__.co_freevars # returns ('count',)

fn1.__closure__ # returns (<cell at 0x0000023093FA6288: int object at 0x00007FFD8C016270>,)
fn2.__closure__ # returns (<cell at 0x0000023093FA6288: int object at 0x00007FFD8C016270>,)

fn1() # return 1 

fn1.__closure__ # returns (<cell at 0x000001980C926288: int object at 0x00007FFD8C016290>,)
fn2.__closure__ # returns (<cell at 0x000001980C926288: int object at 0x00007FFD8C016290>,)
# we can see that the object reference to both the closure changed, when we called the function fn1. So now when we call fn2 it should return 2 

fn2() # return 2 --> Note it returns 2 and not 1 which shows that they share the same closure 

# Case : 
def pow(n):
    def inner(x):
        return x**n

    return inner 

square = pow(2)
square.__closure__ # returns (<cell at 0x000001889FEC2318: int object at 0x00007FFD8C0162B0>,)
square(10) # returns 100 

cube = pow(3)
cube.__closure__ # returns (<cell at 0x000001889FEC2378: int object at 0x00007FFD8C0162D0>,)
cube(3)  # returns 27
# we can see that they are both referencing to differnt object location, i.e they are under different free variable scopes  

#case:  Bewareee!!!
def adder(n):
    def inner(x):
        return x + n 

    return inner 

add_1 = adder(1)
add_2 = adder(2)
add_3 = adder(3)
# they are 3 different closures

add_1.__closure__  # returns (<cell at 0x000001C2ABCF26D8: int object at 0x00007FFD8C016290>,)
add_2.__closure__  # returns (<cell at 0x000001C2ABCF2648: int object at 0x00007FFD8C0162B0>,)
add_3.__closure__  # returns (<cell at 0x000001C2ABCF2618: int object at 0x00007FFD8C0162D0>,)

#so, they will work as expected as : 
add_1(10) # return 11 
add_2(10) # return 12
add_3(10) # return 13 

#But seeing this redundancy of typing, we might wanna run a loop in the following way:

def create_adders():
    adders = []
    for n in range(1, 4):
        adders.append(lambda x: x + n)  
    return adders 

adders = create_adders()
adders[0](10)  # return 13
adders[1](10)  # return 13
adders[2](10)  # return 13
#this is happening because we are creating closures that references the same n, (because we are just creating the function and not calling the function),
#so at the time of calling, it takes the last value of n(which is 3 in our case). This is same as above case of : single reference multi closures 

# so when the adders are created they are pointing to the same object memory addreess, we can check that:
adders[0].__closure__  # returns (<cell at 0x000001D8D36DC318: int object at 0x00007FFD7F8A62D0>,)
adders[1].__closure__  # returns (<cell at 0x000001D8D36DC318: int object at 0x00007FFD7F8A62D0>,)
adders[2].__closure__  # returns (<cell at 0x000001D8D36DC318: int object at 0x00007FFD7F8A62D0>,)

#so when we call adders[0][10], adders[1][10], adders[2][10] -- > the value of n and x is same for all the three hence the same output 

#how to solve this problem?

def create_adders():
    adders = []
    for n in range(1, 4):
        adders.append(lambda x, y=n: x + y)  
    return adders 

"""
This will work because defaults parameters of a function gets evaluated at the creation time, so when this lambda is created the default value of
y(which is changing as n is changing) will be used to create the function. 
But now, y is no longer a free variable, so we are not creating closures, we are creating functions. 
"""

#another way to do this is
adders = []
for n in range(1, 4):
    adders.append(adder(n))

adders[0](10)  # return 11
adders[1](10)  # return 12
adders[2](10)  # return 13

adders[0].__closure__ # returns (<cell at 0x000002346743C378: int object at 0x00007FFD88D46290>,)

#Applications of closure: Given a number calculate the average

#approach 1
class Averager:

    def __init__(self):
        self.numbers = []

    def add(self, number):
        self.numbers.append(number)
        total = sum(self.numbers)
        count = len(self.numbers)
        return total/count

a = Averager()

a.add(10) # return 10.0
a.add(20) # return 15.0
a.add(30) # return 20.0

#approach 2
class Averager:

    def __init__(self):
        self.total = 0
        self.count = 0

    def add(self, number):
        self.total += number
        self.count += 1
        return self.total/self.count

a = Averager()

a.add(10) # return 10.0
a.add(20) # return 15.0
a.add(30) # return 20.0

#Using closure to do the same as we did above
#approach 1
def averager():
    numbers = []

    def add(number):
        numbers.append(number)
        total = sum(numbers)
        count = len(numbers)
        return total/count

    return add 

a = averager()

result = a(10)  # return 10.0
result = a(20)  # return 15.0
result = a(30)  # return 20.0

#approach 2
def averager():
    total = 0 
    count = 0

    def add(number):
        nonlocal total
        nonlocal count 
        total = total + number
        count = count + 1

        return total/count
        
    return add 

a = averager()

result = a(10)  # return 10.0
result = a(20)  # return 15.0
result = a(30)  # return 20.0

import time 

class Timer:

    def __init__(self):
        self.start = time.time()

    def __call__(self): # instance which gets created is callable. 
        return  time.time() - self.start

t1 = Timer() # we can create an object, which we can can just call whenever we want to see the time elapsed. 
# time.sleep(0.1)
result = t1() # return 0.10086560249328613

#using closure to so the same 

def timer():

    start = time.time()
    def poll():
        return time.time() - start
    return poll

t2 = timer()
time.sleep(0.12) 
result = t2() # returns 0.12093043327331543

#2nd Application of closure

def Counter(initial_value):
    def inc(increment = 1):
        nonlocal initial_value
        initial_value += increment 
        return initial_value 
    
    return inc

counter1 = Counter(0)

result = counter1() #returns 1
result = counter1() #returns 2 

#keeping a track of how many times a function has been called
func_counters = dict()

def Counter(fn):
    count = 0

    def inner(*args, **kwargs):
        nonlocal count
        count+=1

        #keeping of track of how many times a function has been called using a global variable 
        func_counters[fn.__name__] = count
        return fn(*args, **kwargs)
    
    return inner

def add(a,b):
    return a + b 

def mult(a,b):
    return a * b  

counter_add = Counter(add)
counter_mult = Counter(mult)

result = counter_add.__code__.co_freevars # returns ('count', 'fn')

result = counter_add(10,20) #returns 30
result = counter_add(30,40) #returns 70

result = counter_mult(30,40) #returns 1200
result = counter_mult(10,20) #returns 200

func_counters # returns {'add': 2, 'mult': 2}

"""Decorators"""
func_counters = {}

def Counter(fn):
    count = 0

    def inner(*args, **kwargs):
        nonlocal count
        count+=1
        
        func_counters[fn.__name__] = count
        return fn(*args, **kwargs)
    
    return inner

def add(a: int, b:int= 0)-> int:
    """
    adds two values 
    """
    return a+b 

add.__doc__ #returns  "adds two values"
add.__annotations__ #returns {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}

id(add) # return 2162418271504 
add = Counter(add)
id(add) # 2162418272184

result = add(10, 20) # returns 30
func_counters# returns {'add': 1}

"""
we can see that the id of add has changed, i.e they are not the same function but can still perform the addition. 
help(add) -->returns inner(*args, **kwargs), which means that we have lost the original annotations and docstrings of the function add, In order to take care of this 
python provides a wrap fucntion which we can import from functools. 
Also, there is an alternate way to add a decorator to the function i.e using a "@" symbol
for example: 
"""

@Counter
def mult(a: int, b:int= 1)-> int:
    """
    multiply two values 
    """
    return a*b 

result = mult(3,4) # returns 12

func_counters # return {'add': 1, 'mult': 1}

#The annotation and doctring problem can be solved in multiple way: Method 1

func_counters = {}

def Counter(fn):
    count = 0

    def inner(*args, **kwargs):
        nonlocal count
        count+=1
        
        func_counters[fn.__name__] = count
        return fn(*args, **kwargs)
    
    inner.__name__ = fn.__name__
    inner.__doc__ = fn.__doc__
    inner.__annotations__ = fn.__annotations__
    return inner

def mult(a: int, b:int= 1)-> int:
    """
    multiply two values 
    """
    return a*b 

mult = Counter(mult)

mult.__doc__   #returns  multiply two values
mult.__name__   #returns  mukt
mult.__annotations__   #returns  {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}

#Method 2 
from functools import wraps 

func_counters = {}

def Counter(fn):
    count = 0

    def inner(*args, **kwargs):
        nonlocal count
        count+=1
        
        func_counters[fn.__name__] = count
        return fn(*args, **kwargs)
    
    wraps(fn)(inner) # takes the original function to decorate the inner function
    return inner

def mult(a: int, b:int, c:int= 1)-> int:
    """
    multiply three values 
    """
    return a*b*c

mult = Counter(mult)

"""
help(mult)  ---> mult(a: int, b: int, c: int = 1) -> int
                     multiply three values
""" 

#Applications of Timer 

def timed(fn):
    import time 
    from functools import wraps

    @wraps(fn) # this is a parameterised wrapper i.e the output of the decorator is a function
    def inner(*args, **kwargs):
        elapsed_total = 0 
        elapsed_count = 0 

        for i in range(10):
            start = time.time()
            result = fn(*args, **kwargs)
            end = time.time()
            elapsed = end - start

            elapsed_total +=elapsed 
            elapsed_count +=1

        args_ = [str(a) for a in args]
        kwargs_ = ["{0}={1}".format(k, v) for k, v in kwargs.items()]
        all_args = ",".join(args_ + kwargs_)

        print("{0}({1}) took an average {2:.6f}s to run".format(fn.__name__, 
                                                    all_args, 
                                                    elapsed_total/elapsed_count))
        return result

    return inner 

@timed
def recursive_fibb(n, memoised = {}):
    if n <= 2:
        return 1 
    else:
        return recursive_fibb(n-1) + recursive_fibb(n-2)


@timed
def looped_fibb(n):
    if n <= 2:
        return 1 
    
    i = 1
    j = 1
    for k in range(3, n+1):
        i, j = j, i + j 

    return j

from functools import reduce 

@timed 
def fib_reduce(n):
    initial = (1,1)
    fib_n = reduce(lambda prev, n: (prev[0]+ prev[1], prev[0]), range(3,n+1), initial)  
    return fib_n[0]

# commented because decorator has a print function

# recursive_fibb(3)
# looped_fibb(10000)
# fib_reduce(10000)

#Application 2 of Decorators 

def logged(fn):
    from functools import wraps
    from datetime import datetime, timezone
    @wraps(fn)
    def inner(*args, **kwargs):
        run_dt = datetime.now(timezone.utc)
        result = fn(*args, **kwargs)
        print("{0}: called {1}".format(run_dt, fn.__name__))
        
        return result
    
    return inner

@logged
def func1():
    pass 

@logged
def func2():
    pass 

# we can pass multiple decorators, but the order in which we pass will affect the result. 
@logged
@timed
def fact(n):
    from functools import reduce 
    return reduce(lambda x, y : x*y, range(1, n+1))

# fact(5)
# func1()
# func2()


#Using Memoisation for recursion to reduce the timings 
class Fibb:

    def __init__(self):
        self.cache = dict({1:1, 2:1})

    def fib_class(self, n ):
        if n not in self.cache:
            # print("calculating fibb {0}".format(n))
            self.cache[n] = self.fib_class(n-1) + self.fib_class(n-2)

        return self.cache[n]

def fib_closure():
    cache = dict({1: 1, 2: 1})
    def calc_fib(n):
        if n not in cache:
            # print("calculating fibb {0}".format(n))
            cache[n] = calc_fib(n-1) + calc_fib(n-2)
        return cache[n]

    return calc_fib

#using closure 
f = fib_closure()
f(7)

#using class 
f = Fibb()
f.fib_class(7)

#using decorator to do the caching 
def memoize(fn):
    cache = dict()

    def inner(n):
        if n not in cache:
            cache[n] = fn(n)
        return cache[n]
    return inner

@memoize
def fibb_recursion(n):
    # print("calculating fibb {0}".format(n))
    return 1 if n < 3 else fibb_recursion(n-1) + fibb_recursion(n-2)

fibb_recursion(10)
fibb_recursion(12)

#The memoize function is a very generic one, we can use it for anything 
@memoize
def fact(n):
    # print("calculating fact {0}!".format(n))
    return 1 if n < 2 else n * fact(n-1)

fact(10)
fact(11)

#python has an inbuilt caching mechanism 
from functools import lru_cache #lru stands for "least recently used"-> i.e least used are tosssed out of cache memory  

@lru_cache(maxsize = 8) #this is a parameterised decorator, for instance: you can set the maximum cache size 
def fib(n):
    # print("calculating fib {0}".format(n))
    return 1 if n < 3 else fib(n-1) + fib(n-2)

fib(10) # returns 55

"""Parameterised Decorators"""

def dec_factory():

    def dec(fn):
        # print("Decorator running")

        def inner(*args, **kwargs):
            print("inner running")
            return fn(*args, **kwargs)

        return inner

    return dec 

@dec_factory() # same as, my_func = dec_factory()(my_func) 
def my_func():
    print("my_func running")


# my_func()

#let's add paprmeter to the decorator_factory
def dec_factory(a, b):

    def dec(fn):
        # print("Decorator running")

        def inner(*args, **kwargs):
            print("inner running")
            print("a= {}, b={}".format(a, b))
            return fn(*args, **kwargs)

        return inner

    return dec 

@dec_factory(10, 20) # same as, my_func = dec_factory(10, 20)(my_func)
def my_func():
    print("my_func running")

# my_func()

"""
when we write add a decorator using the @ symbol on top of a function as follows: :
@timed
def fact(n):
    from functools import reduce 
    return reduce(lambda x, y : x*y, range(1, n+1))

this is equivalent to writing--> fact = timed(fact)

so now in below parameterised version, which is also known as decorator factory :

@timed(23)
def fact(n):
    from functools import reduce 
    return reduce(lambda x, y : x*y, range(1, n+1))

This is same as this:--> fact = timed(23)(fact) i.e. the output of timed(23) is a decorator which takes fn as an input. 
"""

#let's modify the timed function now, the number of reps would be a parameter in this case, and it will return a decorator which will take fn as an input. 
def timed(reps):

    def dec(fn):
        import time 
        from functools import wraps

        @wraps(fn) 
        def inner(*args, **kwargs):
            elapsed_total = 0 
            elapsed_count = 0 

            for i in range(reps):
                start = time.time()
                result = fn(*args, **kwargs)
                end = time.time()
                elapsed = end - start

                elapsed_total +=elapsed 
                elapsed_count +=1

            args_ = [str(a) for a in args]
            kwargs_ = ["{0}={1}".format(k, v) for k, v in kwargs.items()]
            all_args = ",".join(args_ + kwargs_)

            print("{0}({1}) took an average {2:.6f}s to run {3} times ".format(fn.__name__, 
                                                        all_args, 
                                                        elapsed_total/elapsed_count, reps))
            return result

        return inner 
    return dec 

@timed(23)
def fact(n):
    from functools import reduce 
    return reduce(lambda x, y : x*y, range(1, n+1))

# fact(5) #returns fact(5) took an average 0.000000s to run 23 times

"""Decorator Classes"""
class Myclass:
    def __init__(self, a, b):
        self.a = a 
        self.b = b 

    def __call__(self, fn):
        def inner(*args, **kwargs):
            print("decorated {} with a = {}, b = {}".format(fn.__name__, self.a, self.b))                                             
            return fn(*args, **kwargs)

        return inner 

@Myclass(30,40)
def my_func(s):
    print("Hello {}".format(s))

# my_func("world")

"""Decorating Classes"""
from datetime import datetime, timezone

def info(obj):
    result = []
    result.append("Time: {}".format(datetime.now(timezone.utc)))
    result.append("Class: {}".format(obj.__class__.__name__))
    result.append("Id: {}".format(hex(id(obj))))

    for k, v in vars(obj).items():
        result.append("{0}: {1}".format(k, v))

    return result

def debug_info(cls):
    cls.debug = info 
    return cls

@debug_info
class Person:

    def __init__(self, name, age):
        self.name = name 
        self.age = age 

    def hi(self):
        return "Hello world"

p = Person("Pulkit", 23)
p.debug() # returns ['Time: 2020-07-23 16:09:11.418853+00:00', 'Class: Person', 'Id: 0x11637ebbe10', 'name: Pulkit', 'age: 23']

@debug_info
class Automobile:

    def __init__(self, make, model, year, top_speed):
        self.make = make
        self.model = model
        self.year = year
        self.top_speed = top_speed
        self._speed = 0
    
    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new_speed):
        if new_speed > self.top_speed:
            raise ValueError("Speed cannot exceed top speed")
        else:
            self._speed = new_speed


favourite = Automobile("Hyundai", "Creta", 2020, 180)
result = favourite.debug() # returns ['Time: 2020-07-23 16:16:07.557669+00:00', 'Class: Automobile', 'Id: 0x2412ad9b0b8', 'make: Hyundai', 'model: Creta', 'year: 2020', 'top_speed: 180', '_speed: 0']

favourite.speed = 100
result = favourite.debug() # returns ['Time: 2020-07-23 16:17:12.515880+00:00', 'Class: Automobile', 'Id: 0x1add07fb0b8', 'make: Hyundai', 'model: Creta', 'year: 2020', 'top_speed: 180', '_speed: 100']

import math 

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y 

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __repr__(self):
        return "Point({}, {})".format(self.x , self.y)


p1, p2, p3 = Point(2,3), Point(2,3), Point(0,0)

result = abs(p1) # return 3.605551275463989
result = p1 # return Point(2, 3)

p1==p2 # return False
"""This happens because Python doesn't know how to compare p1 and p2, hence it defaults to comparing memory addresses whoch are differnt"""

#adding __eq__ method
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y 

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __repr__(self):
        return "Point({}, {})".format(self.x , self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x ==other.x and self.y == other.y
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, Point):
            return abs(self) < abs(other)
        else:
            return NotImplemented
    
    def __le__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __ne__(self, other):
        pass
    
p1, p2, p3 = Point(2,3), Point(2,3), Point(0,0)

p1 is p2 # return False 
p1==p2 # return True 

p4 = Point(100,120)

result = p2 < p4
result = p2 > p4 # return False
""" although we have not decalared the greater than method, what python does is check whether p4 < p2 and returns the result,
Also, instead of difining a method for each case, we can built a decorator, which given a fact that we have created equal-to and less-than, 
we can build the remaining""" 

def complete_ordering(cls):
    if "__eq__" in dir(cls) and "__lt__" in dir(cls):
        cls.__le__ = lambda self, other: self < other or self == other
        cls.__gt__ = lambda self, other: not(self < other) and not(self ==other)
        cls.__ge__ = lambda self, other: not(self < other) or self==other
        cls.__ne__ = lambda self, other: not(self==other)
    return cls 

@complete_ordering
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y 

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __repr__(self):
        return "Point({}, {})".format(self.x , self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x ==other.x and self.y == other.y
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, Point):
            return abs(self) < abs(other)
        else:
            return NotImplemented

p1, p2, p3 = Point(2,3), Point(2,3), Point(0,0)

p1 != p2 # return False
p2 != p3 # return True
p1 <= p3 # return False
p1 >= p3 # return True

#python provides a decorator for this too, for which we need to define atleast one of the [__lt__, __gt__] and __eq__ and it will define the rest 
from functools import total_ordering

@total_ordering
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y 

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __repr__(self):
        return "Point({}, {})".format(self.x , self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x ==other.x and self.y == other.y
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, Point):
            return abs(self) < abs(other)
        else:
            return NotImplemented

p1, p2, p3, p4 = Point(2,3), Point(2,3), Point(0,0), Point(100,200)

result = p1 != p2 # return False
result = p2 != p3 # return True
result = p1 <= p3 # return False
result = p1 >= p3 # return True

"""Decorators Application: Single Dispatch Generic functions"""
from html import escape

def html_escape(arg):
    return escape(str(arg))

def html_int(a):
    return "{0}(<i>{1}</i>)".format(a, str(hex(a)))

def html_real(a):
    return '0:.2f'.format(round(a, 2))

def html_str(s):
    return html_escape(s).replace("\n", '<br/>\n')

def html_list(l):
    items = ('<li>{0}</li>'.format(htmlize(item)) for item in l)

    return '<ul>\n' + '\n'.join(items) + '\n</ul>'

def html_dict(d):
    items = ('<li>{0}= {1}</li>'.format(k, htmlize(v)) for k, v in d.items())

    return '<ul>\n' + '\n'.join(items) + '\n</ul>'

from decimal import Decimal 

def htmlize(arg):
    if isinstance(arg, int):
        return html_int(arg)

    if isinstance(arg, float) or isinstance(arg, Decimal):
        return html_real(arg)
    
    if isinstance(arg, str):
        return html_str(arg)
    
    if isinstance(arg, list) or isinstance(arg, tuple):
        return html_list(arg)

    if isinstance(arg, dict):
        return html_dict(arg)
    else:
        return html_escape(arg)


result = htmlize(100) #return 100(<i>0x64</i>)
result = htmlize([1,2,3]) # return    <ul>
                                    # <li>1</li>
                                    # <li>2</li>
                                    # <li>3</li>
                                    # </ul>

result = htmlize(["python", (1,2,3), 100 ])  

"""The problem here is everytime we want to add a new function, we will have to modify the htmlize as well"""
#alternate method

def single_dispatch(fn):
    registry= {}

    registry[object] = fn

    def decorated(arg):
        return registry.get(type(arg), registry[object])(arg)
    
    #to register a new function along with it's datatype into the  registry dictionary. 
    def register(type_):
        def inner(fn):
            registry[type_] = fn
            return fn
        
        return inner

    decorated.register_func = register  #added "register_func", as an attribute to the decorated function which is linked to the register function. 
    decorated.registered_func = registry
    return decorated  

@single_dispatch
def htmlize(arg):
    return escape(str(arg))

result = htmlize("python") #return python

#let's give it a integer type
result = htmlize(100) #return 100
# so now in order to add this to the htmlize : 

@htmlize.register_func(int)
def html_int(a):
    return "{0}(<i>{1}</i>)".format(a, str(hex(a)))

result = htmlize(100) #return 100(<i>0x64</i>)

#similarly 
@htmlize.register_func(tuple)
@htmlize.register_func(list)
def html_sequence(l):
    items = ('<li>{0}</li>'.format(htmlize(item)) for item in l)
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'


result = htmlize([1,2,3]) #return <ul>
                                # <li>1(<i>0x1</i>)</li>
                                # <li>2(<i>0x2</i>)</li>
                                # <li>3(<i>0x3</i>)</li>
                                # </ul>




print(htmlize.registered_func) #return {<class 'object'>: <function htmlize at 0x000002EF76788D90>, <class 'int'>: <function html_int at 0x000002EF76790048>, <class 'list'>: <function html_sequence at 0x000002EF767900D0>, <class 'tuple'>: <function html_sequence at 0x000002EF767900D0>}
# print(result)