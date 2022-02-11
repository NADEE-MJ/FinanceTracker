"""
The goal of this testing module is to berate the server with requests to test how
well it handles ddos attacks and see how well flask_limiter is able to deal within
this, it seems that with the limiter it is able to take over 1000 requests in
rapid succession without breaking down

?change times_to_request in main to up the number of requests made to the server,
?this is currently configured to test the development server on localhost, if you
?want to test anther ip then change base variable in main
"""
import requests, threading


class TestUser:
    def __init__(self, password1: str, password2: str, email: str, username: str):
        self.password1 = password1
        self.password2 = password2
        self.email = email
        self.username = username
        self.access_token = None
        self.refresh_token = None

    # simulate login
    def login(self, access_token: str, refresh_token: str) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token


class RequestThread(threading.Thread):
    def __init__(self, id: int, base: str, json: dict):
        threading.Thread.__init__(self)
        self.id = id
        self.base = base
        self.json = json

    def run(self) -> None:
        # print(f"starting thread#{self.id}")
        response = get_request(self.base, self.json).json()
        if type(response) == list:
            print(response)
        # print(f"ending thread#{self.id}")


def get_request(base, json):
    return requests.get(base + "stocks", json=json)


def main():
    base = "http://localhost:5000/"

    user = TestUser(
        "ddospassword", "ddospassword", "ddosemail@email.com", "ddosusername"
    )

    json = {
        "email": user.email,
        "username": user.username,
        "password1": user.password1,
        "password2": user.password2,
        "password": user.password1,
    }
    # register user
    response = requests.post(base + "user", json=json)
    print(response.json())

    # login user and get access_token
    response = requests.put(base + "user", json=json)
    print(response.json())

    # save access_token
    data = {
        "access_token": response.json().get("access_token", {}),
        "refresh_token": response.json().get("refresh_token", {}),
    }
    user.login(data["access_token"], data["refresh_token"])
    json["access_token"] = user.access_token

    # create threads and run them
    threads = []
    times_to_request = 1000
    for i in range(times_to_request):
        threads.append(RequestThread(id=i, base=base, json=json))

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    print("main thread done")


if __name__ == "__main__":
    main()
