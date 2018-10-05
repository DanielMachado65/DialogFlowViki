from flask import Blueprint

from app.main.utils import list_all_intents

processo = Blueprint('processo', __name__)


# TODO: fazer o CRUD da aplicação
@processo.route('/processo/main', methods=['POST', 'GET'])
def main():
    list_all_intents('small-talk-c36ba')
    return 'ok', 200
