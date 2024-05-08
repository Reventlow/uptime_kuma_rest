import requests

url = 'http://127.0.0.1:8000/uptime_kuma/api-token-auth/'
data = {'username': 'gore', 'password': 'FGD88axb'}

response = requests.post(url, data=data)
print(response.text)  # This will print the token if authentication was successful
