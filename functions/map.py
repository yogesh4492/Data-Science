""" Map Function that map the result based on function 
its contain two parameter:

map(function,iterable)
their is function based map the data 
by default its return map object convert it into list also for working

difference beetween map and filter is map pnly apply the condition or function on the iterable like list,tuple,and 
set but filter can take result by filetr the function conditions
"""

def double(w):
    return w*2
lis=[1,2,3,4,5]
res=map(double,lis)
print(list(res))


""" Map With Lambdas """

result=map(lambda x: x**2 ,lis)
print(list(result))


"""Map with list comprehensive and lmdas """

lis3=[a for a in range(1,50)]
result=filter(lambda x: x%2==0,lis3)
print(list(result))


""" Map with multiple result """
lis1=[10,20,30,40,50]
lis2=[1,2,3,4,5]
resu=map(lambda x,y:x*y,lis1,lis2)
print(list(resu))


""" Converting syring to upper case uing map """

lis=['yogesh','ram','rahul','manhar']
res=map(str.upper ,lis)
print(list(res))


""" Extracking first character from each string in list using map"""

res=list(map(lambda x: x[0],lis))
res1=map(str.upper,res)
print(list(res1))


"""  Removing whitespace from each string in list """

lis=['   Yogesh   ','    Yash    ','   arjun   ','   karn   ']
print(lis)
res=map(str.strip,lis)
print(list(res))

