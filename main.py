from fastapi import FastAPI
from fastapi import Header


api = FastAPI()


credentials = {
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine"
}


def authentication(login: str):
    result = False
    user, password = login.split(':')
    try:
        if credentials[user] == password:
            result = True
    except Exception:
        pass
    return result


@api.get('/')
def get_index(Authorization=Header()):
    if authentication(Authorization):
        return {
            'auth': 'ok'
        }
    else:
        return {
            'auth_error': 'merci de vous authentifier'
        }
