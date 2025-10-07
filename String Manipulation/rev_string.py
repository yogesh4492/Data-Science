string="Python"
# with out the slicing 
rev=""
for i in string:
    rev= i+rev
print(rev)

#with use of slicing
rev1=string[::-1]
print(rev1)


#now time to check string is palindrome or not

string=input("Enter The String= ")
if string== string[::-1]:
    print(f"{string} is palindome  string ")
else:
    print(f"{string} is not  palindrome String")
    

