from flask_restful import abort

from flask import Flask, redirect, session, request
from flask import render_template as flask_render_template
import extra.auth as auth
from api.v1 import init as init_api_v1
from forms import *

from models import User, Character, Post


def init_route(app, db):

    # Переопределение стандартного рендера, добавляет параметр auth_user
    def render_template(*args, **kwargs):
        kwargs['auth_user'] = auth.get_user()
        return flask_render_template(*args, **kwargs)

    init_api_v1(app, auth)  # Инициализация маршрутов для API

    @app.route('/')
    @app.route('/index')
    def index():
        if not auth.is_authorized():
            return render_template(

                'index.html',
                title='Главная',
            )
        # ВОЗВРАЩАЕТ ГЛАВНУЮ СТРАНИЦУ ЧЕРЕЗ НОВУЮ ФУНКЦИЮ И НОВЫЙ ШАБЛОН
        return redirect('/main')


    # ФУНКЦИЯ, КОТОРАЯ ОТОБРАЖАЕТ ГАВНУЮ СТРАНИЦУ СО ВСЕМИ ПЕРСОНАЖАМИ
    @app.route('/main', methods=['GET'])
    def main_list():
        if not auth.is_authorized():
            return redirect('/login')
        character_list = Character.query.all()

        return render_template(
            'main-list.html',
            title='Персонажи',
            character_list=character_list
        )



    @app.route('/install')
    def install():
        db.create_all()
        User.add(username='admin', password='admin', admin=True)
        return render_template(
            'install-success.html',
            title="Главная"
        )

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        has_error = False
        login = ''
        if request.method == 'POST':
            username = request.form['username']
            if auth.login(username, request.form['password']):
                return redirect('/')
            else:
                has_error = True
        return render_template(
            'login.html',
            title='Вход',
            login=login,
            has_error=has_error
        )

    @app.route('/logout', methods=['GET'])
    def logout():
        auth.logout()
        return redirect('/')

    @app.route('/user/create', methods=['GET', 'POST'])
    def registration():
        has_error = False
        form = UserCreateForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user:
                has_error = True
            else:
                User.add(username=username, password=password, admin=False)
                auth.login(username, password)
                return redirect('/character/create')
        return render_template(
            'registration.html',
            title='Зарегистрироваться',
            form=form,
            has_error=has_error
        )

    @app.route('/characters', methods=['GET'])
    def characters_list():
        if not auth.is_authorized():
            return redirect('/login')
        character_list = Character.query.filter_by(user_id=auth.get_user().id)
        messages = Post.query.filter_by(to=auth.get_user().username)
        return render_template(
            'character-list.html',
            title="Персонажи",
            character_list=character_list,
            messages=messages,
        )

    @app.route('/character/create', methods=['GET', 'POST'])
    def character_create_form():
        if not auth.is_authorized():
            return redirect('/login')
        form = CharacterCreateForm()
        if form.validate_on_submit():
            name = form.name.data
            title = form.title.data
            city = form.city.data
            age = form.age.data
            info = form.info.data
            ispublic = form.ispublic.data
            Character.add(name=name, title=title, city=city, age=age, info=info, ispublic=ispublic, user=auth.get_user())
            return redirect('/characters')
        return render_template(
            'character-create.html',
            title='Создать новость',
            form=form
        )

    @app.route('/characters/<int:id>')
    def characters_view(id: int):
        if not auth.is_authorized():
            return redirect('/login')
        character = Character.query.filter_by(id=id).first()
        if not character:
            abort(404)
        if character.user_id != auth.get_user().id and not character.ispublic:
            abort(403)
        user = character.user
        return render_template(
            'character-view.html',
            title='Персонаж - ' + character.title,
            character=character,
            user=user
        )

    @app.route('/character/delete/<int:id>')
    def characters_delete(id: int):
        if not auth.is_authorized():
            return redirect('/login')
        character = Character.query.filter_by(id=id).first()
        if character.user_id != auth.get_user().id:
            abort(403)
        Character.delete(character)
        return redirect('/characters')

    @app.route('/sendmessage', methods=['GET', 'POST'])
    def send_message():
        if not auth.is_authorized():
            return redirect('/login')
        form = WriteMessageForm()
        if form.validate_on_submit():
            receiver_id = request.args.get('sel')
            user = User.query.filter_by(id=receiver_id).first()
            message = form.message.data
            Post.add(from_who=auth.get_user().username, to=user.username, message=message, user=auth.get_user())
            return redirect('/main')
        return render_template(
            'message-write.html',
            title='Написать сообщение',
            form=form
        )

