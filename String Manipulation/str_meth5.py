""" String Methods Like 
1) Strip
2) lstrip
3) rstrip
"""

#strip That Remove White space Or Any Chara from The rigt and aleft side of string

str1="  hello "#here whitespace
print(str1)
print(str1.strip())#by default its remove the space

str2="---hello---"
print(str2)
print(str2.strip())#its not remove the lines
print(str2.strip('-'))# its remove lines from before and after the string


# rstrip remove from the right side only by default its space 
# l strip is remove whitespace from the starting only

