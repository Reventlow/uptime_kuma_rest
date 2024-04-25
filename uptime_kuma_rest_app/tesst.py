import requests
import json

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

# Convert dictionary to JSON string
json_data = json.dumps(data)

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer d8dd34fb6539564c053ba993d7574df4eeee6ff5"
}

# Send POST request
response = requests.post(url, data=json_data, headers=headers)

# Print response
print(response.text)
