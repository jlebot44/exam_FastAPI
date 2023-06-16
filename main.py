import pandas as pd
from fastapi import FastAPI
from fastapi import Header
import random
from pydantic import BaseModel


api = FastAPI(
    title="Questionnaire technique",
    description="Questionnaire technique réalisé dans le cadre du module FastAPI",
    version="1.0"
)


credentials = {
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine"
}


class Questionary(BaseModel):
    """A questionary with parameters"""
    use: str
    subject: str
    number: int


def authentication(login: str):
    result = False
    user, password = login.split(':')
    try:
        if credentials[user] == password:
            result = True
    except Exception:
        pass
    return result


def generate_questionary(use : str, subject : str, indice : int):
    df = pd.read_csv('data/questions.csv')
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
        index_question = random.randint(0,indice-1)
        if liste_questions[index_question][4] != 'nan':
            questionnaire.append({
                'question': liste_questions[index_question][0],
                'reponse A' : liste_questions[index_question][1],
                'reponse B' : liste_questions[index_question][2],
                'reponse C' : liste_questions[index_question][3],
                'reponse D' : liste_questions[index_question][4]
            })
        else:
            questionnaire.append({
                'question': liste_questions[index_question][0],
                'reponse A' : liste_questions[index_question][1],
                'reponse B' : liste_questions[index_question][2],
                'reponse C' : liste_questions[index_question][3]
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


@api.get('/questions', name='Nouveau Questionnaire', tags=['all'])
def get_index(questionary_type: Questionary, Authorization=Header(description="login:password")):
    """Returns a questionary with a list of questions"""
    if authentication(Authorization):
        indice = questionary_type.number
        use = questionary_type.use
        subject = questionary_type.subject
        questionary = generate_questionary(use,subject, indice)
        return questionary 
    else:
        return {
            'auth_error': 'merci de vous authentifier'
        }
