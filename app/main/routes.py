import json

import dialogflow_v2 as dialogflow
from flask import render_template, Blueprint, request

from app import db
from app.models.models_sql_alchemy import Request, Response

main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
@main.route('/home')
def home():
    # GET params json.
    req = request.get_json(silent=True, force=True)
    if req and request.method == 'POST':
        if req.get("session"):
            if req.get("texto") and req.get("name"):
                request_user = Request(
                    session=req.get("session"),
                    name=req.get("name"),
                    id=req.get("id"),
                    text=req.get("texto"))

                db.session.add(request_user)
                db.session.commit()

                # HACK: pegar da API o retorno.
                retorno = detect_intent_texts(project_id='small-talk-c36ba', session_id=request_user.session,
                                              texts=request_user.text, language_code='pt-br')

                response = Response(
                    action=retorno.get('action'),
                    intentDetectionConfidence=retorno.get('intentDetectionConfidence'),
                    fulfillmentText=retorno.get('fulfillmentText'),
                    parent_id=request_user.session
                )

                db.session.add(response)
                db.session.commit()

                return json.dumps({
                    "action": response.action,
                    "response": response.fulfillmentText
                }, indent=4).encode('utf-8')
            else:
                return json.dumps(
                    error_type(error="Não foi encontrado uma id e Texto", session=req.get("session"))).encode('utf-8')
        else:
            return json.dumps(error_type(error="Não foi informado uma Sessão", session='')).encode('utf-8')
    else:
        return render_template('home.html', title="::admin::",
                               list_all=Request.query.all()), 200


@main.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return 'banco resetado'


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
