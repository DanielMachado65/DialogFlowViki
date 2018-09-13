import json

import dialogflow_v2 as dialogflow
from flask import Blueprint, render_template, request

processo = Blueprint('processo', __name__)


@processo.route('/processo', methods=['POST', 'GET'])
def processoMain():
    req = request.get_json(silent=True, force=True)
    if req:
        print('Request: ' + json.dumps(req, indent=4))
        if req.get("queryResult").get("action") == "workflow.processo":
            print('Está sendo lidado com um processo')

        elif req.get("queryResult").get("action") == "workflow.card":
            print('Está sendo liado com um card')
        else:
            print('Não está sendo lidado com um processo reconhecido')
        return render_template('home.html', title="Processo", texto=json.dumps(req, indent=4))
    else:
        return render_template('home.html', title='Processo',
                               texto=detect_intent_texts(project_id='small-talk-c36ba', session_id=12,
                                                         texts='abrir um proceso', language_code='pt-br'))


@processo.route('/processo/export')
def export():
    if export_agent_for_zip():
        return 'ok'
    return 'not ok'


@processo.route('/processo/agent')
def agent():
    if get_agent('small-talk-c36ba'):
        return 'ok'
    return 'not ok'


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))
    text_input = dialogflow.types.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    print('-_-' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    return 'Frase Verificada: {} Detected intent: {} (confidence: {})\n'.format(
        response.query_result.fulfillment_text,
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence)


def export_agent_for_zip():
    client = dialogflow.AgentsClient()
    parent = client.project_path('small-talk-c36ba')
    for element in client.search_agents(parent):
        print(element)

    return True


def get_agent(project_id):
    client = dialogflow.AgentsClient()
    parent = client.project_path(project_id)
    agent = client.get_agent(parent)
    print(agent)
    return parent


def callback(operation_future):
    result = operation_future.result()
    return result
