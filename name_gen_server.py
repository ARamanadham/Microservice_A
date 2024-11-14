import random
import zmq
import json


# Expanded consonants and vowels
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'qu', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'th', 'ch', 'sh', 'ph']
vowels = ['a', 'e', 'i', 'o', 'u', 'ae', 'ei', 'ie', 'oo', 'ea', 'ou', 'ue']

# Titles for names
titles = ['the Brave', 'the Wise', 'Stormborn', 'Lightbringer', 'Shadowdancer']

def build_name(pattern):
    result = ''
    for char in pattern:
        if char == 'C':
            result += random.choice(consonants)
        elif char == 'V':
            result += random.choice(vowels)
    return result

def add_special_character(name):
    if random.random() < 0.3:  # 30% chance
        index = random.randint(1, len(name) - 1)
        char = random.choice(["'", "-"])
        return name[:index] + char + name[index:]
    return name

def generate_name(race=None):
    if race == 'elf':
        patterns = ['CVCV', 'CVVCV', 'VCVV']
    elif race == 'dwarf':
        patterns = ['CVCC', 'CCVC', 'CVCVC']
    else:
        patterns = ['CV', 'CVC', 'CVCC', 'CVCV', 'CVVCV', 'CCVC', 'VCV']
    
    name_length = random.randint(1, 4)
    name = ''.join(build_name(random.choice(patterns)) for _ in range(name_length))
    name = add_special_character(name)
    return name.capitalize()

def fantasy_name(name_num=None, race=None, add_title=False):
    if name_num is None:
        name_num = random.randint(1, 3)
    
    if add_title is False:
        add_title = random.choices([True, False], weights=[3, 7])
    
    full_name = []
    for _ in range(name_num):
        full_name.append(generate_name(race))
    
    full_name = ' '.join(full_name)
    
    if add_title and random.random() < 0.3:  # 30% chance to add a title
        full_name += ' ' + random.choice(titles)
    
    return full_name

# Set up ZeroMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5324")

print("Fantasy name generator server is running...")

while True:
    message = socket.recv_json()
    print(f"Received request: {message}")
    
    name_num = message.get('name_num')
    race = message.get('race')
    add_title = message.get('add_title', False)
    
    name = fantasy_name(name_num=name_num, race=race, add_title=add_title)
    
    socket.send_string(name)
    print(f"Sent name: {name}")