import json

import dialogflow_v2 as dialogflow
from flask import render_template, Blueprint, request

from app import db
from app.models.models import RequestUser

main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
@main.route('/home')
def home():
    # GET params json.
    req = request.get_json(silent=True, force=True)
    if req and request.method == 'POST':
        if req.get("session"):
            if req.get("texto") and req.get("name"):
                return json.dumps(detect_intent_texts(
                    project_id='small-talk-c36ba',
                    session_id=req.get("session"),
                    texts=req.get("texto"),
                    language_code='pt-br'), indent=4).encode('utf-8')
            else:
                return json.dumps(error_type(error="", session=req.get("session"))).encode('utf-8')
        else:
            return json.dumps(error_type(error="Não foi informado uma Sessão", session='')).encode('utf-8')
    else:
        return render_template('home.html', title="Home Default"), 200


def error_type(error, session):
    if session and error:
        return {"error": error, "session": session}
    elif error:
        return {"error": error}
    else:
        return {"Error": "Aconteceu algum tipo de error que não foi possivel ser resolvido"}


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))
    text_input = dialogflow.types.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    return {
        "action": response.query_result.intent.display_name,
        "intentDetectionConfidence": response.query_result.intent_detection_confidence,
        "fulfillmentText": response.query_result.fulfillment_text
    }
