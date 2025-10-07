""" In this we can check the string is Contain Vowel Or Not And Also Count Vowel """


string = input("Enter The String= ")
status=False
no_of_vowels=0
for i in string:
    if i in 'aeiou':
        status=True
        no_of_vowels+=1
if status:
    print("String Contain Vowel")
    print(f"Total no Of Vowel In String is = {no_of_vowels}")

else:
    print("No Vowel present In String ")
