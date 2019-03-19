from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, RadioField, SelectField
from wtforms.validators import DataRequired


class CharacterCreateForm(FlaskForm):
    name = StringField('', validators=[DataRequired()])
    title = RadioField('', choices=[('Арбор', '-------- Арбор ----------'), ('Туг', '----------- Туг -----------'),
                                    ('Панголины', '------- Панголины ------'), ('Фодинис', '-------- Фодинис ---------'),
                                    ('Люди', '--------- Люди ----------')], validators=[DataRequired()])
    city = SelectField('', choices=[('Эвендор', 'Эвендор'), ('Крагос', 'Крагос'), ('Серфилиус', 'Серфилиус'),
                                    ('Георам', 'Георам'), ('Каварна', 'Каварна'), ], validators=[DataRequired()])
    age = StringField('', validators=[DataRequired()])
    info = TextAreaField('')
    ispublic = BooleanField('')
    submit = SubmitField('Создать')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class UserCreateForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Создать')
