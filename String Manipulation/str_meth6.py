""" 
String Methods like 
replace & expanding """

#replace methods that replace character or substring of string with old to n ew
# name='yogesh'
string=f"hello My name is Yogesh "
print("Demo String = ",string)
choice=input("If you Want To check Your Name And Preview The String Press 'y' or Yes= ").lower()
print(choice)
if choice=='y' or choice=='yes':

    name1=input("Enter you name = ")
    print(string.replace('Yogesh',name1))
else:
        print("Thank You")


    