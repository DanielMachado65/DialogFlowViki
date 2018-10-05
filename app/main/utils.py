from unicodedata import normalize

import dialogflow_v2 as dialogflow


def error_type(error, session):
    if session and error:
        return {"error": error, "session": session}
    elif error:
        return {"error": error}
    else:
        return {"Error": "Aconteceu algum tipo de error que não foi possivel ser resolvido"}


def remover_acentos(text):
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def callback(operation_future):
    print('--' * 10)
    print('Result')
    result = operation_future.result()
    print(result)
    # todo: fazer com que reset o banco logo após aprender sobre as funções.
    # redirect(url_for('main.reset'))


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return {
        "action": response.query_result.intent.display_name,
        "intentDetectionConfidence": response.query_result.intent_detection_confidence,
        "fulfillmentText": response.query_result.fulfillment_text
    }


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    """ Criar uma intenção ."""
    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    response = intents_client.create_intent(parent, intent)

    print('Intent created: {}'.format(response))


def list_all_intents(project_id):
    client = dialogflow.IntentsClient()
    parent = client.project_agent_path(project_id)
    for texto in client.list_intents(parent):
        print(texto)