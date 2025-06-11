import can
import time
import os

# Create logs directory (../logs) relative to this file
log_dir = os.path.join(os.path.dirname(__file__), '../logs')
os.makedirs(log_dir, exist_ok=True)

# Create a new log file with a timestamp
log_file = os.path.join(log_dir, f"session_{int(time.time())}.log")

# Initialize CAN interface (use 'interface' instead of deprecated 'bustype')
bus = can.interface.Bus(channel='vcan0', interface='socketcan')

print(f"Logging CAN messages to {os.path.abspath(log_file)}...\n")

with open(log_file, 'w') as f:
    try:
        while True:
            msg = bus.recv(1.0)  # Timeout after 1 second
            if msg:
                log_line = f"{msg.timestamp:.6f} ID:{hex(msg.arbitration_id)} DLC:{msg.dlc} DATA:{msg.data.hex()}"
                print(log_line)
                f.write(log_line + '\n')
                f.flush()  # Write immediately
    except KeyboardInterrupt:
        print("\nStopped logging.")
