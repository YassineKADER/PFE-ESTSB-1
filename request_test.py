import requests
import json
data = open('img.png','rb').read()

file = {'file' : open('img.png','rb')}

r = requests.post("http://127.0.0.1:1212/perviewimg",files=file)

print(r.text)