import json

with open("config.json") as file:
    data = json.load(file)

print(data)