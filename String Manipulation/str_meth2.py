""" String Methods Like 
1) Find 
2) rfind
3) index
4) rindex"""


string1=input("Enter String 1 = ")
string2=input("Enter String 2 = ")
sub=input("Enter Character to find= ")
sub2=input("Enter The Word fo find= ")

print(string1.find(sub))# its return -1 if not found
print(string1.find(sub2))
print(string2.find(sub))
print(string2.find(sub2))


# rfind methods

print(string1.rfind(sub))# its return -1 if not found
print(string1.rfind(sub2))
print(string2.rfind(sub))
print(string2.rfind(sub2))



# Index Method that can search from start to end 

# print(string1.index(sub))# its return valueerror if not found
# print(string1.index(sub2))
# print(string2.index(sub))
# print(string2.index(sub2))

#rindex method that can search from right to left


print(string1.rindex(sub))# its return valueerror if not found
print(string1.rindex(sub2))
print(string2.rindex(sub))
print(string2.rindex(sub2))


