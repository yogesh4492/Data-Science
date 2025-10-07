""" Types of recursion :

Mainly Two Types : 
1) Tail Recursion:-
its just like loop but give the final result 
2) Non-Tail Recursion:- 
its like yield or accumulate give the result avery time when function call itself
# base case its most important if you want to ignore the infinite recursion

"""
def tail_fact(n, acc=1):
    # Base case
    if n == 0:
        return 0
    elif n==1:
        return acc
    # Tail recursive call with an accumulator
    else:
        return tail_fact(n-1, acc + n)+tail_fact(n-2,acc+n)

def nontail_fact(n):
    # Base case
    if n==0:
        return 0
    if n == 1:
        return 1
    # Non-tail recursive call because the multiplication happens after the call
    else:
        return nontail_fact(n-2) + nontail_fact(n-1)

# Example usage
print(tail_fact(5))  
print(nontail_fact(10))