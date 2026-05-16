import requests

url = "http://127.0.0.1:18789/v1/chat/completions"

headers = {
    "Authorization": "Bearer f23c96f649011b5f1aefc3a3a645a44d8e12eb3fe3944a69",
    "Content-Type": "application/json"
}

data = {
    "model": "openclaw",
    "messages": [
        {
            "role": "user",
            "content": "Hello"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.text)