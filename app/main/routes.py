import json

import dialogflow_v2 as dialogflow
from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required

from app import db, list_chamada
from app.main.forms import LoginForm
from app.models.models_sql_alchemy import Request, Response, Admin

main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
@main.route('/home')
def home():
    # GET params json.
    req = request.get_json(silent=True, force=True)
    if req and request.method == 'POST':
        if req.get("id"):
            if req.get("texto") and req.get("name"):
                request_user = Request(
                    name=req.get("name"),
                    id_user=req.get("id"),
                    text=req.get("texto"))

                db.session.add(request_user)
                db.session.commit()

                # HACK: pegar da API o retorno.
                retorno = detect_intent_texts(project_id='small-talk-c36ba', session_id=request_user.id_user,
                                              texts=request_user.text, language_code='pt-br')

                response = Response(
                    action=retorno.get('action'),
                    intentDetectionConfidence=retorno.get('intentDetectionConfidence'),
                    fulfillmentText=retorno.get('fulfillmentText'),
                    parent_id=request_user.id_request
                )

                db.session.add(response)
                db.session.commit()

                return json.dumps({
                    "action": response.action,
                    "response": response.fulfillmentText
                }, indent=4).encode('utf-8')
            else:
                return json.dumps(
                    error_type(error="Não foi encontrado Nome e Texto", session=req.get("session"))).encode('utf-8')
        else:
            return json.dumps(error_type(error="Não foi informado uma Id", session='')).encode('utf-8')
    else:
        return redirect(url_for('main.gerenciamento'))


@main.route('/gerenciamento', methods=["POST", "GET"])
@main.route('/admin', methods=["POST", "GET"])
@login_required
def gerenciamento():
    return render_template('home.html', title="::admin::",
                           list_all=Request.query.all()), 200


@main.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@gmail.com" and (form.password.data == "root" or form.password.data == "123"):
            # IDEA: mudar para uma coisa mais segura
            admin = Admin.query.filter_by(email=form.email.data).first()
            print(admin)
            login_user(admin)
            flash("Você foi logado com sucesso", "success")
            return redirect(url_for('main.home'))
        else:
            flash("Nao foi possivel logar. Por favor entre em contato com o administrador do sistema", "danger")
    return render_template('login.html', title="Login", form=form)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.gerenciamento'))


@main.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    admin = Admin(email="admin@gmail.com", password="root")
    db.session.add(admin)
    db.session.commit()
    flash("O Banco foi resetado com sucesso", "success")
    return redirect(url_for('main.gerenciamento'))


@main.route("/<int:request_id>/validar")
def validar(request_id):
    list_chamada.append(Request.query.get(request_id))
    flash(str(Request.query.get(request_id)) + str(len(list_chamada)), "warning")
    return redirect(url_for('main.home'))


@main.route("/<int:request_id>/delete")
def delete(request_id):
    request = Request.query.get_or_404(request_id)
    db.session.delete(request)
    db.session.commit()
    flash(" O Banco foi atualizado com a nova validação", 'success')
    return redirect(url_for('main.home'))


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
    text_input = dialogflow.types.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return {
        "action": response.query_result.intent.display_name,
        "intentDetectionConfidence": response.query_result.intent_detection_confidence,
        "fulfillmentText": response.query_result.fulfillment_text
    }
