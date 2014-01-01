import sys, pygame, re, json

#So the idea is that you have a list of dictionaries from which you want
#to make a list of objects. Let's start with a simpler example.

#Here's a dictionary with two things in it.
dict = {"number 1":5, "number 2":13}

#Here's how you access the first number
print dict["number 1"]

#and now the second number
print dict["number 2"]

#now let's talk about arrays for a bit

#here's an array with 4 elements
array = [23, 42, 87, 99]

print array[0] #prints 23
print array[2] #prints 87
#print array[4] would cause an error if it wasn't commented out

#The easiest way to do something with all the elements in this array
#is to use a for loop
for element in array:
    print element
#in this example the for loop is called 4 times.
#The first time element is 23, the next time it's 42, and so on.

#Ok, now lets talk about objects for a bit
#Here's a simple class, which is a blueprint for the creation of objects
class Simple_Class(object):
    def __init__(self, number1, number2):
        self.number1 = number1
        self.number2 = number2

#The first line is a class definition, the (object) bit says that this class
#inherits from the object class, which is the highest object in the class
#class heirarchy.

#The second line is the beginning of Simple_Class's constructor. All
#constructors in python are named __init__. All the constructor does is 
#create new variables in Simple_Class called number1 and number2 and assigns
#them the values of the parameters (number1 and number2) in the constructor.

#Now we can do something like this:
simple_object = Simple_Class(dict["number 1"], dict["number 2"])
#if the above line confuses you just look at the code above or email me

#We can access the numbers in simple object using this syntax
print simple_object.number1
print simple_object.number2

#but We wanted an array of Game objects created from an array of 
