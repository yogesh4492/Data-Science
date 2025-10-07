""" String Indexing means access the string character from the by index"""
#positive index start with 0 its give first char
#negative index start with -1 its give last char


string="Hello How Are you"
#positive indexing
print(string[0])#that print the first char
print(string[1])#that print the second char of string
print(string[len(string)-1])#last char
print(string[len(string)-2])#second last char 


#negative indexing

print(string[-1])#last 
print(string[-2])#second last
print(string[-len(string)])#first
second=-len(string)
print(string[second+1])#its print second char using negativ index

