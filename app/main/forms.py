from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList
from wtforms.validators import DataRequired, Email, ValidationError, required


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_username(self, username):
        if username != "admin@gmail.com":
            raise ValidationError('O usuário não é o correto, por favor entre em contato com o administrador. ')


class Intent(FlaskForm):
    name = StringField('Nome Entidade', validators=[DataRequired()])
    response = FieldList(StringField('Respostas', validators=[required()]))
    submit = SubmitField('Criar uma nova Inteção')