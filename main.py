from fastapi import FastAPI
from fastapi import Header
from typing import Optional

api = FastAPI()


credentials = {
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine"
}

def authentication(login : str):
    result = False
    user = login.split(':')[0]
    password = login.split(':')[1]
    try:
        if credentials[user] == password:
            result = True 
    except:
        pass
    return result 


@api.get('/')
def get_index(custom_header: Optional[str] = Header(None)):
    if authentication(custom_header):     
        return {
            'auth' : 'ok'
        }
    else:
        return {
            'auth_error' : 'merci de vous authentifier'
        }




