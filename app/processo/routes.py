import dialogflow_v2 as dialogflow

from flask import Blueprint, render_template

processo = Blueprint('processo', __name__)


@processo.route('/processo')
def processoMain():
    return render_template('home.html',
                        texto=detect_intent_texts(project_id='small-talk-c36ba', session_id=12, texts='abrir um proceso', language_code='pt-br'))




def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))
    text_input = dialogflow.types.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    print('-_-' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    return 'Frase Verificada: {} <hr><br> Detected intent: {} (confidence: {})\n'.format(
        response.query_result.fulfillment_text,
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence)
