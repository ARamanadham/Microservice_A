import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5324")

# Example requests
requests = [
    {"name_num": 2, "race": "elf", "add_title": True},
    {"name_num": 1, "race": "dwarf", "add_title": False},
    {"name_num": 3, "add_title": True},
    {}  # Default parameters
]

for req in requests:
    socket.send_json(req)
    name = socket.recv_string()
    print(f"Generated name: {name}")