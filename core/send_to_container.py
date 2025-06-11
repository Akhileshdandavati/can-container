import re
import subprocess

# Define operator precedence (similar to CAN ID priorities)
PRIORITY = {"mult": 1, "div": 1, "add": 2, "sub": 2}

def parse_equation(equation):
    # Convert math symbols to function names
    equation = equation.replace("*", " mult ").replace("/", " div ")
    equation = equation.replace("+", " add ").replace("-", " sub ")

    # Split into tokens (numbers and operators)
    tokens = equation.split()

    # Convert numbers to float and store as tuples (operator, num1, num2)
    operations = []
    i = 1
    while i < len(tokens) - 1:
        num1, op, num2 = float(tokens[i-1]), tokens[i], float(tokens[i+1])
        operations.append((PRIORITY[op], op, num1, num2))
        i += 2

    # Sort operations by priority (like CAN arbitration)
    operations.sort()
    
    return operations

def send_to_container(operation, num1, num2):
    cmd = f"sudo lxc-attach -n mycontainer -- python3 /root/cal.py {operation} {num1} {num2}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def evaluate_expression(equation):
    operations = parse_equation(equation)
    
    while len(operations) > 1:
        _, op, num1, num2 = operations.pop(0)  # Get the highest priority operation
        result = float(send_to_container(op, num1, num2))  # Perform the calculation
        operations.insert(0, (0, "add", result, operations[0][3]))  # Store the result

    return operations[0][2]  # Final result

if __name__ == "__main__":
    equation = input("Enter a math expression: ")
    result = evaluate_expression(equation)
    print(f"Final result: {result}")
