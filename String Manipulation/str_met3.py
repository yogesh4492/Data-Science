"""
string methods like

1) count
2) startswith
3) endswith
4) membership Operatrs (in ,not in)
"""

#count the word or charcter how many time appear in string
string =input("Enter String= ")
ch=input("Enter Any Character or Word for count= ")
print(string.count(ch))


#Startswith and endswith method that can check the url or gmail ids 
string2=input("Enter url= ")
if string2.startswith("https://") or string2.startswith("http://"):
    if string2.endswith(".com") or string2.endswith(".co") or string2.endswith(".in"):
        print("Valid Url")
    else:
        print("Make Sure Url End With Specific Domain")
else:
    print("Port Not Found")


# member ship operator valid any sub string is present in main string or not
string3=input("Enter String3 = ")
sub=input("Enter Sub String For Check= ")
if sub in string3:
    print("Present in string")
else:
    print("Not Available in string")



