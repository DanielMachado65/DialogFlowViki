import dialogflow_v2 as dialogflow

from flask import Blueprint
from google.cloud import storage

processo = Blueprint('processo', __name__)


@processo.route('/processo')
def processoMain():
    try:
        implicit()
        print('oi')
        # TODO: detect_intent_texts('testebank-9465d', 'rando-string', 'abrir um processo', 'pt-br')
    except Exception as erro:
        print(erro)
    return 'ok'


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))


def implicit():
    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()
    print(storage_client)

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)
