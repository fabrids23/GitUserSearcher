import requests
import json

def make_request(username):
    try:
        response = requests.get(f'https://api.github.com/users/{username}')
        print(response.text)
        return json.loads(response.text)

    except Exception as exc:
        print(exc)
        return Exception
