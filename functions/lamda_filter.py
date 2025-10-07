""" Using For returning multiple result"""

""" Its return multiple result with tuple """

mul=lambda x,y:(x+y,x-y,x*y)
res=mul(4,3)
print(res)


""" Lambda With filter as function """

lis1=[x for x in range(1,21)]
even=filter(lambda x: x%2==0,lis1)
print(list(even))



""" Filtering String From  lis using filter and lamdas based on length of string"""

lis2=['apple','banana','mangoberry']
res=filter(lambda w :len(w)>5 ,lis2)
print(list(res))



