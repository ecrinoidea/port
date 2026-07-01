import urllib.request
import app

with urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=5) as response:
    print(response.status)
    print(response.read().decode())
