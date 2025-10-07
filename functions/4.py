""" Anonymous Funtion : Means Function have no name 
--its defined using "Lamda" keyword """


def cube(x): return x*x*x
squ_re=lambda x: x*x



print(cube(2))
print(cube(-2))# when its cube if argument its negative its give negative result
print(squ_re(2))
print(squ_re(-2))#when its square its convert negative argument to positive result
print(squ_re(-5))
print(squ_re(5))