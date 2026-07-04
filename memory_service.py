import os
import json

MEMORY_PATH = "memory.json"


def load_memory():

    if not os.path.exists(MEMORY_PATH):
        return {}

    with open(MEMORY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def save_memory(memory):
    with open(MEMORY_PATH, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)


def remember_fact(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)


def recall_fact(key):
    memory = load_memory()
    return memory.get(key)

# remember_fact("manager", "Raj")

# print(recall_fact("manager"))