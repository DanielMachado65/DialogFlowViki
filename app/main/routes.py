# coding: utf-8
import json

import dialogflow_v2 as dialogflow
from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required

from app import db, list_chamada
from app.main.forms import LoginForm, Intent
from app.main.utils import error_type, remover_acentos, callback, detect_intent_texts
from app.models.models_sql_alchemy import Request, Response, Admin

main = Blueprint('main', __name__)


# TODO: ESSA PARTE VAI PERGUNTAR E TREINAR A APLICAÇÃO
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
                }, indent=4, ensure_ascii=False).encode("utf8")
            else:
                return json.dumps(
                    error_type(error="Não foi encontrado Nome e Texto", session=req.get("session")),
                    ensure_ascii=False).encode('utf8')
        else:
            return json.dumps(error_type(error="Não foi informado uma Id", session='')).encode('utf8')
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
    request_s = Request.query.get(request_id)
    if request_s:
        resposta = request_s.response[0].fulfillmentText
        print(resposta)
        list_chamada.update({str(request_id): remover_acentos(resposta)})
        print(list_chamada)
        flash(json.dumps(list_chamada, ensure_ascii=False).encode("utf8"), "warning")
        # return json.dumps(list_chamada, ensure_ascii=False).encode("utf8")
        return redirect(url_for('main.home'))
    else:
        return print('not ok')


@main.route("/<int:request_id>/create_intent")
def create_intent_route(request_id):
    request_s = Request.query.get_or_404(request_id)
    if not current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form_request = Intent()
    print(request_s)
    form_request.name.data = request_s.response[0].action
    return render_template('new.html', title='Criar uma nova Inteção', form=form_request)


@main.route("/<int:request_id>/delete")
def delete(request_id):
    request_user = Request.query.get_or_404(request_id)
    db.session.delete(request_user)
    db.session.commit()
    flash(" O Banco foi atualizado com a nova validação", 'success')
    return redirect(url_for('main.home'))


@main.route('/trainAgent')
def train():
    print('--' * 10)
    print('Foi adicionado ao treinamento')
    client = dialogflow.AgentsClient()
    parent = client.project_path('small-talk-c36ba')
    try:
        print(list_chamada)
        response = client.train_agent(parent=parent, metadata=list_chamada.items())
        response.add_done_callback(callback)
    except Exception as error:
        print(error)
    return redirect(url_for('main.gerenciamento'))
