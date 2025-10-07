"""Combining lambda with List Comprehension"""

#list comprehension means sort way to create list
#normal list comprehension
odd=[x for x in range(1,10,2)]
print(odd)


#with lambda

s1=[lambda args=x: args for  x in range(0,10,2)]# even numbers
for i in s1:
    print(i())
