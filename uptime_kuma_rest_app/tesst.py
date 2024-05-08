import requests

# API endpoint
url = "http://127.0.0.1:8000/uptime_kuma/api/heartbeats/receive/"

# Data to be sent to API
data = {
    "heartbeat": {
        "status": "up",
        "timestamp": "2021-08-01T12:00:00Z",
        "error": None
    },
    "monitor": {
        "id": 1,
        "name": "Example Monitor",
        "type": "http",
        "url": "http://example.com",
        "interval": 60
    },
    "msg": "Monitor is up"
}

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token 7a3af99fb748ab47583c8f04952bac6d7bb91296"
}

# Send POST request
response = requests.post(url, json=data, headers=headers)

# Print response
print(response.text)
