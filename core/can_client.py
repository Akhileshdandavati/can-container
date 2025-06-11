import can

OP_CODES = {
    "add": 0,
    "sub": 1,
    "mult": 2,
    "div": 3
}

# Ask for user input
op_name = input("Enter operation (add, sub, mult, div): ").strip().lower()
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

op_code = OP_CODES.get(op_name, 0)  # Default to add

bus = can.interface.Bus(interface='socketcan', channel='vcan0')

# Format: [op_code, num1, num2, 0, 0, 0, 0, 0]
msg = can.Message(arbitration_id=0x300,
                  data=[op_code, num1, num2, 0, 0, 0, 0, 0],
                  is_extended_id=False)

print(f"Sending CAN message: {op_name}({num1}, {num2})")
bus.send(msg)
bus.shutdown()
