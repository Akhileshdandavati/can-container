# CAN Bus Container Offload System

This project simulates a simple automotive system where messages are sent over a virtual CAN bus, and specific messages trigger math operations that are offloaded to a Linux container for processing.

It is built using Python, SocketCAN (`vcan0`), and LXC (Linux Containers). This setup is useful to understand how ECUs (Electronic Control Units) can communicate over a CAN network and offload tasks to other systems.

---

## How the System Works

1. The `can_client.py` script sends CAN messages on the virtual CAN interface.
2. The `can_offload_listener.py` script listens for specific messages (ID `0x300`) and reads the operation type and operands from the message data.
3. When a valid message is received, the operation is sent to a container (`mycontainer`) using `lxc-attach`, where the math is performed.
4. The result is returned to the host and printed on the screen. It is also saved in a log file.
5. All CAN traffic can also be logged using `can_logger.py`.

---

## CAN Message Format

The CAN message sent to trigger a container operation has:
- **Arbitration ID**: `0x300`
- **Data Bytes**:
  - Byte 0: operation code (`0=add`, `1=sub`, `2=mult`, `3=div`)
  - Byte 1: first number
  - Byte 2: second number

Example:
```
ID: 0x300
DATA: 02 03 04
→ mult(3, 4)
```

---

## Project Files and Folders

```
can-container/
├── core/
│   ├── can_client.py            # Sends a CAN message based on user input
│   └── send_to_container.py     # Sends math operations to container
├── tools/
│   ├── can_logger.py            # Logs all messages on vcan0 to a file
│   └── can_offload_listener.py  # Listens for trigger messages and handles offloading
├── container_code/
│   └── cal.py                   # This is the script that runs inside the container
├── logs/                        # Contains result logs
├── .gitignore
└── README.md
```

---

## Container Setup

### 1. Container Requirements
Inside your LXC container (`mycontainer`), place the following script as `/root/cal.py`. This script receives operation type and two numbers via command-line arguments.

The `container_code/cal.py` file in this repository is the exact same script used inside the container.

### 2. How to copy `cal.py` into container
From host:
```bash
sudo lxc-attach -n mycontainer
```

Inside the container:
```bash
mkdir -p /root
# Use `nano /root/cal.py` and paste the code, or copy from shared volume
chmod +x /root/cal.py
exit
```

---

## How to Set Up and Run

### 1. Set up virtual CAN interface (host)
Run this once each time the VM starts:

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

---

### 2. Start the container (if not already running)
```bash
sudo lxc-start -n mycontainer -d
```

---

### 3. Run the listener (host)
```bash
python3 tools/can_offload_listener.py
```

This will wait for CAN messages with ID `0x300`.

---

### 4. Send a CAN message (host)
```bash
python3 core/can_client.py
```

This will ask for:
- Operation type (add, sub, mult, div)
- Two numbers

It will then send a CAN message in the correct format.

---

### 5. (Optional) Run CAN logger
```bash
python3 tools/can_logger.py
```

This logs all traffic on the virtual CAN interface to a log file inside `logs/`.

---

## Requirements

- Linux (tested on Ubuntu 20.04/22.04)
- Python 3.8+
- python-can
- LXC (Linux Containers)
- SocketCAN (vcan0)

Install requirements:
```bash
sudo apt install lxc python3-pip
pip3 install python-can
```


---

## License

This project is open-source and free to use for learning and demonstration purposes.
