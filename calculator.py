# Simple Calulator 
print("Welcome to Simple Calculator Operations")

def add(a,b):
    return a+b
def sub(a,b):
    return a-b
def mul(a,b):
    return a*b
def div(a,b):
    return a/b

print('1 - Add')
print('2 - Subtraction')
print('3 - Multiply')
print('4 - Divide')
print('5 - Exit')

option = int(input("Choose an operation :"))
if(option==5):
    print("GoodBye! Exiting from the operation")
else:
    if(option in [1,2,3,4]):
        num1 = int(input("Enter the first number:"))
        num2 = int(input("Enter the second number:"))
        if(option==1):
            res = add(num1,num2)
        elif(option==2):
            res = sub(num1,num2)
        elif(option==3):
            res = mul(num1,num2)
        elif(option==4):
            res = div(num1,num2)
        print(f"The result of the operation is {res}")
    else:
        print("Invalid operation choosed...!")
