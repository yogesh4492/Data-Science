""" Default Argument """

def Argument(x,y=100):
    print(x,y)
Argument(10,111)
Argument(11)
Argument(11,12)# error :TypeError

""" Keyword Argument """
def Keyword(x,y):
    print(x,y)

Keyword(x=10,y=20)
Keyword(y=40,x=30)

""" Positional Argument """

def Positional(name,age):
    print("My Name is ",name)
    print("My Age IS ",age)
Positional('yogesh',20)
Positional(20,'yogesh')# its print wrong data because postion is change


""" Arbitary Argument  """

def Arbitary(*args,**kwargs):
    for i in args:
        print(i,end=" ")
    for k,v in kwargs.items():
        print(f"{k} is {v} ",end=" ")
    print()
    return
    

Arbitary("hello",'my',name='yogesh',age=25)
Arbitary("Hello",'how','are','you')
Arbitary(name='Ram',age=25)

