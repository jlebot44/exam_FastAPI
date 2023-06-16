import pandas as pd
from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse
import random
from pydantic import BaseModel
import datetime


df = pd.read_csv('data/questions.csv')

use_labels = df['use'].unique()
subject_labels = df['subject'].unique()
nb_questions = [5, 10, 20]

api = FastAPI(
    title="Questionnaire technique",
    description="Questionnaire technique \
                 réalisé dans le cadre du module FastAPI",
    version="1.0"
)

credentials = {
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine"
}

responses = {
    200: {"description": "tout bon"},
    418: {"description": "use exception :\
           choose a subject in this list : " + str(use_labels)},
    419: {"description": "subject exception :\
           choose a subject in this list : " + str(subject_labels)},
    420: {"description": "number exception :\
            choose an number in this list : " + str(nb_questions)},
    421: {"description": "authentication exception"}
}


class Questionary(BaseModel):
    """A questionary with parameters"""
    use: str
    subject: str
    number: int


class CustomAuthenticationException(Exception):
    """A custom class for Exception description"""
    def __init__(self, name: str, date: str):
        self.name = name
        self.date = date


class CustomUseException(Exception):
    """A custom class for Exception description"""
    def __init__(self, name: str, date: str):
        self.name = name
        self.date = date


class CustomSubjectException(Exception):
    """A custom class for Exception description"""
    def __init__(self, name: str, date: str):
        self.name = name
        self.date = date


class CustomNumberException(Exception):
    """A custom class for Exception description"""
    def __init__(self, name: str, date: str):
        self.name = name
        self.date = date


def authentication(login: str):
    result = False
    user, password = login.split(':')
    try:
        if credentials[user] == password:
            result = True
    except Exception:
        pass
    return result


def generate_questionary(use: str, subject: str, indice: int):
    liste_questions = []
    questions = df[(df['use'] == use) & (df['subject'] == subject)]
    if indice > len(questions):
        indice = len(questions)

    for i in range(indice):
        liste_questions.append([str(questions['question'].iloc[i]),
                                str(questions['responseA'].iloc[i]),
                                str(questions['responseB'].iloc[i]),
                                str(questions['responseC'].iloc[i]),
                                str(questions['responseD'].iloc[i])])
    questionnaire = []
    while indice > 0:
        index_question = random.randint(0, indice-1)
        if liste_questions[index_question][4] != 'nan':
            questionnaire.append({
                'question': liste_questions[index_question][0],
                'reponse A': liste_questions[index_question][1],
                'reponse B': liste_questions[index_question][2],
                'reponse C': liste_questions[index_question][3],
                'reponse D': liste_questions[index_question][4]
            })
        else:
            questionnaire.append({
                'question': liste_questions[index_question][0],
                'reponse A': liste_questions[index_question][1],
                'reponse B': liste_questions[index_question][2],
                'reponse C': liste_questions[index_question][3]
            })
        liste_questions.pop(index_question)
        indice -= 1

    return questionnaire


@api.get('/', tags=['all'])
def get_index(Authorization=Header()):
    """test authentication"""
    if authentication(Authorization):
        return {
            'auth': 'ok'
        }
    else:
        return {
            'auth_error': 'merci de vous authentifier'
        }


@api.get('/questions', name='Nouveau Questionnaire', responses=responses, tags=['all'])
def get_questionary(questionary_type: Questionary,
                    Authorization=Header(description="login:password")):
    """Returns a questionary with a list of questions"""
    if authentication(Authorization):
        indice = questionary_type.number
        use = questionary_type.use
        subject = questionary_type.subject
        if indice not in nb_questions:
            raise CustomNumberException(
                name='count error, please choose an number in this list : '+ str(nb_questions),
                date=str(datetime.datetime.now()))
        elif use not in use_labels:
            raise CustomUseException(
                name='use error, please choose a subject in this list : ' + str(use_labels),
                date=str(datetime.datetime.now()))
        elif subject not in subject_labels:
            raise CustomSubjectException(
                name='subject error, please choose a subject in this list : ' + str(subject_labels),
                date=str(datetime.datetime.now()))
        else:
            questionary = generate_questionary(use, subject, indice)
            return questionary
    else:
        raise CustomAuthenticationException(
            name='Authentication error ! Please, add your login:password in the head of yout resuqest',
            date=str(datetime.datetime.now()))


@api.exception_handler(CustomUseException)
def MyExceptionHandler(
    request: Request,
    exception: CustomUseException
    ):
    return JSONResponse(
        status_code=418,
        content={
            'url': str(request.url),
            'name': exception.name,
            'message': 'This error is my own',
            'date': exception.date
        }
    )


@api.exception_handler(CustomSubjectException)
def MyExceptionHandler(
    request: Request,
    exception: CustomSubjectException
    ):
    return JSONResponse(
        status_code=419,
        content={
            'url': str(request.url),
            'name': exception.name,
            'message': 'This error is my own',
            'date': exception.date
        }
    )


@api.exception_handler(CustomNumberException)
def MyExceptionHandler(
    request: Request,
    exception: CustomNumberException
    ):
    return JSONResponse(
        status_code=420,
        content={
            'url': str(request.url),
            'name': exception.name,
            'message': 'This error is my own',
            'date': exception.date
        }
    )


@api.exception_handler(CustomAuthenticationException)
def MyExceptionHandler(
    request: Request,
    exception: CustomAuthenticationException
    ):
    return JSONResponse(
        status_code=421,
        content={
            'url': str(request.url),
            'name': exception.name,
            'message': 'This error is my own',
            'date': exception.date
        }
    )
