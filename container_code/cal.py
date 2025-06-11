import sys

def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def mult(x, y):
    return x * y

def div(x, y):
    return x / y if y != 0 else "Error: Division by zero"

def calculate(op, x, y):
    operations = {
        "add": add,
        "sub": sub,
        "mult": mult,
        "div": div
    }
    if op in operations:
        return operations[op](x, y)
    return "Error: Invalid operation"

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 cal.py <operation> <num1> <num2>")
        sys.exit(1)
    
    operation, num1, num2 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    result = calculate(operation, num1, num2)
    print(result)