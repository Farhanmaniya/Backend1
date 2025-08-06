import requests

url = "http://127.0.0.1:8000/hackrx/run"
headers = {
    "Authorization": "Bearer 9da8aafea3dc4af423a86e812d47c130c9d39985a93d5f6574705dbf192d0209",
    "Content-Type": "application/json"
}
data = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
    "Are the medical expenses for an organ donor covered under this policy?"
    ]

}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.json())
