import requests
import json
print(json.loads(requests.get(url="http://127.0.0.1:1313/status").text).get("status"))