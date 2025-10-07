"""Nested Function : Function Within Function Its Called nested Function """

def s1():
    s='Hello My Name'
    def s2():
        print(f"{s.upper()} IS {name.upper()}")
    s2()

name=input("Enter user Name : ")
s1()