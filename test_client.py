import requests
url = "http://127.0.0.1:5000/encrypt"
payload = {"message":"HELLO","key":"3","algorithm":"Caesar Cipher"}
r = requests.post(url, json=payload, timeout=5)
print("status:", r.status_code)
print("text:", r.text)
print("json:", r.json())
