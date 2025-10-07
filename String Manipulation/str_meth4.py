""" String Methods like 
spliting and joining most important in real word 

1) split()
2) rsplit()
3) splitlines()
4) partition()
5) rpartition()
6) join()
"""

#split that can by default split the string into list of word by space you can also able to give any separator 


string="hello How Are You"
print(string.split())# by default space 

string2="My/Name/Is/Yogesh/Patel"
list1=string2.split('/')
print(list1)#that can split by /

print(len(list1))#that print how many word in string

#join method that rejoin the string based on separator from the list

str2=" ".join(list1)
print(str2)