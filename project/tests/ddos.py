import requests, threading


class TestUser:
    def __init__(self, password1, password2, email, username):
        self.password1 = password1
        self.password2 = password2
        self.email = email
        self.username = username
        self.access_token = None
        self.refresh_token = None

    def login(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token

    def refresh_access_token(self, access_token):
        self.access_token = access_token


class RequestThread(threading.Thread):
    def __init__(self, id, base, params):
        threading.Thread.__init__(self)
        self.id = id
        self.base = base
        self.params = params

    def run(self):
        # print(f'starting thread#{self.id}')
        response = get_request(self.base, self.params).json()
        if type(response) == list:
            print(response)
        # print(f'ending thread#{self.id}')


def get_request(base, params):
    return requests.get(base + "stocks", json=params)


def main():
    base = "http://localhost:5000/"

    user = TestUser(
        "ddospassword", "ddospassword", "ddosemail@email.com", "ddosusername"
    )

    params = {
        "email": user.email,
        "username": user.username,
        "password1": user.password1,
        "password2": user.password2,
        "password": user.password1,
    }
    response = requests.post(base + "user", json=params)
    print(response.json())

    response = requests.put(base + "user", json=params)
    print(response.json())

    data = {
        "access_token": response.json().get("access_token", {}),
        "refresh_token": response.json().get("refresh_token", {}),
    }
    user.login(data["access_token"], data["refresh_token"])

    params["access_token"] = user.access_token

    threads = []
    times_to_request = 2000
    for i in range(times_to_request):
        threads.append(RequestThread(id=i, base=base, params=params))

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    print("main thread done")


if __name__ == "__main__":
    main()
