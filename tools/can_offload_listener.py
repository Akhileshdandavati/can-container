import can
import subprocess
import os
import time

OP_MAP = {
    0: "add",
    1: "sub",
    2: "mult",
    3: "div"
}

def send_to_container(operation, num1, num2):
    cmd = f"sudo lxc-attach -n mycontainer -- python3 /root/cal.py {operation} {num1} {num2}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

# Setup log directory
log_dir = os.path.join(os.path.dirname(__file__), '../logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"offload_log_{int(time.time())}.txt")

bus = can.interface.Bus(channel='vcan0', interface='socketcan')

print(f"Logging offload results to {log_file}")
print("Listening for math trigger messages on CAN bus (ID 0x300)...\n")

with open(log_file, 'w') as log:
    try:
        while True:
            msg = bus.recv()
            if msg.arbitration_id == 0x300:
                op_code = msg.data[0]
                num1 = msg.data[1]
                num2 = msg.data[2]
                op = OP_MAP.get(op_code, "add")

                print(f"Received operation: {op}({num1}, {num2})")
                result = send_to_container(op, num1, num2)
                print(f"➡️  Result from container: {result}\n")

                log.write(f"{time.ctime()} | {op}({num1}, {num2}) = {result}\n")
                log.flush()
    except KeyboardInterrupt:
        print("\nListener stopped.")
