import requests
from concurrent.futures import ThreadPoolExecutor

def send_request(data, url, headers=None):
    return requests.post(url, json=data, headers=headers)

url = "https://example.com/api"
payload = {"foo": "bar"}

with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [
        executor.submit(send_request, payload, url),
        executor.submit(send_request, payload, url)
    ]

responses = [f.result() for f in futures]

for i, r in enumerate(responses):
    print(f"Response {i+1}: {r.status_code} - {r.text}")
