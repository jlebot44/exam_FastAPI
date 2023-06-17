import pandas as pd
from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse
import random
from pydantic import BaseModel
import datetime
from typing import Optional


df = pd.read_csv('data/questions.csv')
data_file = "data/questions.csv"

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

admin_credentials = {
    "admin": "4dm1N"
}

responses = {
    200: {"description": "Ok"},
    418: {"description": "Use exception :\
           choose a subject in this list : " + str(use_labels)},
    419: {"description": "Subject exception :\
           choose a subject in this list : " + str(subject_labels)},
    420: {"description": "Number exception :\
            choose an number in this list : " + str(nb_questions)},
    421: {"description": "Authentication exception"},
    422: {"description": "Admin authentication exception"}
}


class Questionary(BaseModel):
    """A questionary with parameters"""
    use: str
    subject: str
    number: int


class Question(BaseModel):
    """A question to add in the database"""
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: str
    responseD: Optional[str] = ""
    remark: Optional[str] = ""


class CustomException(Exception):
    """A custom class for Exception description"""
    def __init__(self, name: str, date: str, code: int, message: str):
        self.name = name
        self.date = date
        self.code = code
        self.message = message


def authentication(login: str):
    result = False
    user, password = login.split(':')
    try:
        if credentials[user] == password:
            result = True
    except Exception:
        pass
    return result


def admin_authentication(login: str):
    result = False
    user, password = login.split(':')
    try:
        if admin_credentials[user] == password:
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


@api.get('/',
         name='check API status',
         tags=['all'])
def get_index():
    """test API state"""
    return "API is running"


@api.get('/questions',
         name='New questionary',
         responses=responses,
         tags=['all'])
def get_questionary(questionary_type: Questionary,
                    Authorization=Header(description="login:password")):
    """Returns a questionary with a list of questions"""
    if authentication(Authorization):
        indice = questionary_type.number
        use = questionary_type.use
        subject = questionary_type.subject
        if indice not in nb_questions:
            raise CustomException(
                name='count error',
                date=str(datetime.datetime.now()),
                code=420,
                message='count error, please choose an number in this list : '
                        + str(nb_questions))
        elif use not in use_labels:
            raise CustomException(
                name='use error',
                date=str(datetime.datetime.now()),
                code=418,
                message='use error, please choose a subject in this list : '
                        + str(use_labels))
        elif subject not in subject_labels:
            raise CustomException(
                name='subject error',
                date=str(datetime.datetime.now()),
                code=419,
                message='subject error, please choose a subject in this list : '
                        + str(subject_labels))
        else:
            questionary = generate_questionary(use, subject, indice)
            return questionary
    else:
        raise CustomException(
            name='Authentication error',
            date=str(datetime.datetime.now()),
            code=421,
            message='Authentication error ! Add login:password'
                    ' in the head of your request')


@api.post('/add_question',
          name='Add question',
          responses=responses,
          tags=['admin'])
def add_question(question: Question,
                 Authorization=Header(description="login:password")):
    if admin_authentication(Authorization):
        with open(data_file, 'a') as file:
            file.write(question.question + ',' +
                       question.subject + ',' +
                       question.use + ',' +
                       question.correct + ',' +
                       question.responseA + ',' +
                       question.responseB + ',' +
                       question.responseC + ',' +
                       question.responseD + ',' +
                       question.remark)
            file.write('\n')
            file.close()
        return "question successfully added"
    else:
        raise CustomException(
            name='Admin Authentication error',
            date=str(datetime.datetime.now()),
            code=422,
            message='Admin Authentication error ! Add login:password'
                       ' in the head of your request')


@api.exception_handler(CustomException)
def MyCustomUseExceptionHandler(request: Request,
                                exception: CustomException):
    return JSONResponse(
        status_code=exception.code,
        content={
            'url': str(request.url),
            'name': exception.name,
            'message': exception.message,
            'date': exception.date
        }
    )
