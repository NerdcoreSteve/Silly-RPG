import sys, pygame, re, json

#let's say I have an array of numbers, and I want to double each of their values.

array = [1, 2, 3, 4, 5]

#I'm not sure how familiar you are with array indexes but if you type
print array[0]
#you'll get 1

#if you type
print array[3]
#you'll get 4

#if you type print array[100] you'll get an error
#I'd like this code to run so I'll keep it commented out

#You can also use a variable as an index
i = 3
print array[i] #this will print 4
i = 4
print array[i] #this will print 4

#So if I want to double each of the array's values I could do it this way
array[0] = array[0] * 2
array[1] = array[1] * 2
array[2] = array[2] * 2
array[3] = array[3] * 2
array[4] = array[4] * 2

#that works as far as it goes but it's pretty tiresome
#also it becomes difficult when your array gets big.
#What if your array has 100 or 1000 items?

#So, in your email you referenced the while loop
i = 5
while i > 2:
    print i
    i -= 1 #this statment is the same as i = i - 1
    print "I can put anything I want in here."
    print "Anything in this block will execute as many times, "
    print "as the condition in the while loop (i > 2) is true."

print "After that it stops repeating."
print "The 4 indented lines above repeat 3 times."
print "These three print statements don't repeat."

#Here's one way to loop through the arrays
i = 4
while i >= 0:
    array[i] = array[i] * 2
    print array[i]
    i -= 1

#But there's a problem
#What if you don't know how big your array is?
#We're making a game that has a json file. That file will be editable by
#the user. They can make any number of field objects. We won't know in
#advance how many objects there will be.

#Thankfully this comes up often enough that almost all languages have
#a syntax for looping through a list of elements. In python it's their
#version of the for loop
print "loop"
for array_element in array:
    print array_element
print "loop"
for array_element in array:
    array_element *= 2
for array_element in array:
    print array_element
