# python_deepDive part 2 
# python version: 3.7.3

"""
This module contains the following:
    1. sequences : They have "positional ordering" i.e A list is a sequence, set it not.         
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

"""This happened because, what python did is  -> since the objects were immutable the id(x) is same as id(a[0]) and id(a[1]), so when we modify one value, all the values 
got mutated.
same thing happens in case of repeatation as well, for example: a = [[0, 0]] * 2
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

print(result)
