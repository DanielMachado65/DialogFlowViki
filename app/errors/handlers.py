from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Erro 404 - Clique aqui para voltar', errors=error), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html',  title='Erro 403 - Clique aqui para voltar', error=error), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html',  title='Erro 500 - Clique aqui para voltar', error=error), 500
