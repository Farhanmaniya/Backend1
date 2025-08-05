# test_local.py
import requests

API_URL = "http://127.0.0.1:8000/hackrx/run"
HEADERS = {
    "Authorization": "Bearer 9da8aafea3dc4af423a86e812d47c130c9d39985a93d5f6574705dbf192d0209",
    "Content-Type": "application/json"
}

data = {
    "documents": "https://example.com/sample.pdf",
    "questions": [
        "What is the policy coverage?",
        "Is there a waiting period?"
    ]
}

response = requests.post(API_URL, headers=HEADERS, json=data)
print(response.status_code)
print(response.json())
