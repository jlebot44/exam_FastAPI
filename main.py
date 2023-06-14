from fastapi import FastAPI



api = FastAPI()

credentials = {
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine"
}


@api.get('/')
def get_index():
    return {
        'greetings': 'welcome'
    }
