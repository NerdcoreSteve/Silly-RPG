import sys, pygame, re, json

#if you run this code by typing
#python lesson1.py | more
#you'll be able to see all of the output by pressing the
#return key or space bar.

#So the idea is that you have a list of dictionaries from which you want
#to make a list of objects. Let's start with a simpler example.

#Here's a dictionary with two things in it.
dict = {"number 1":5, "number 2":13}

#Here's how you access the first number
print "Number 1 of dict"
print dict["number 1"]

#and now the second number
print "\nNumber 2 of dict"
print dict["number 2"]

#now let's talk about arrays for a bit

#here's an array with 4 elements
array = [23, 42, 87, 99]

print "\nelements 0 and 2 of array"
print array[0] #prints 23
print array[2] #prints 87
#print array[4] would cause an error if it wasn't commented out

#The easiest way to do something with all the elements in this array
#is to use a for loop
print "\nPrinting each element of array"
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
print "\nPrinting number1 and number2 of simple_object"
print simple_object.number1
print simple_object.number2

#but We wanted an array of Field_Object objects created from an array of
#dictionaries. Let's start with a simple array of dictionaries:
dict_array = [{"number 1":5, "number 2":13},
              {"number 1":4, "number 2":108},
              {"number 1":202, "number 2":347},
              {"number 1":0, "number 2":23}]
#In python, all arrays are surrounded by square brackets. Note the square
#brackets around this array. All elements in an array are separated by
#commas. It's more complicated here but each dictionary in this array is
#separated by a comma. And each dictionary has a format as above: the key,
#a colon, the value, and a comma if there is another key:value pair.

#Here's how you would access the second number form the third dictionary
#in the list:
print "\nThe second number of the third element in dict_array"
print dict_array[2]["number 2"]
#dict_array is an array, so we use numbers to access each element in that
#array. dict_array[2] is the third element in dict_array.
#To access the second number in the third element we need to access the
#value with the key "number 2"

#If I wanted to iterate though each element in dict_array I'd do this
print "\nPrinting out each number from each dict in dict_array"
for dict_element in dict_array:
    print dict_element["number 1"]
    print dict_element["number 2"]

#I think I'll leave it here. I'll let you try to figure the rest out.
#Wrestle with this for a bit and, if you're still having trouble, explain
#what you've tried, where you're stuck, ask me questions, etc. :)
