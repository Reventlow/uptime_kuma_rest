import requests

# Define the endpoint you want to access
url = 'http://127.0.0.1:8000/uptime_kuma/some-protected-route/'

# Your obtained token
token = '7a3af99fb748ab47583c8f04952bac6d7bb91296'

# Set the Authorization header with the token
headers = {
    'Authorization': f'Token {token}'
}

# Make the GET request
response = requests.get(url, headers=headers)

# Print the status code and response data
print("Status Code:", response.status_code)
print("Response:", response.json())
