import requests
import time

base = "http://localhost:5000/"

json = {
    "username": "schedulertest",
    "email": "schedulertest@test.com",
    "password1": "password",
    "password2": "password",
    "password": "password",
}

requests.post(base + "user", json=json)

# adds token to the blocklist every minute
while True:
    for i in range(5):
        response = requests.put(base + "user", json=json)
        json["access_token"] = response.json().get("access_token", {})
        requests.delete(base + "user", json=json)

    time.sleep(60)
