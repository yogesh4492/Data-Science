def pass_by_val(val):# it can not change the original value 
    val=10

val=1
pass_by_val(val)
print(val)

def pass_by_ref(val):
    val[0]=25
    
val=[1,2,3,4]
pass_by_ref(val)
print(val)

    
