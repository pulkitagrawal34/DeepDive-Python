"""
This module covers the following:
    1.Scopes --> Local, Global, nonlocal, Nested
    2. Closures  **very very important concept 
    3. Decorators 
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


print(result)
