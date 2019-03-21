from dbase import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)  # будем хранить хэш пароля
    admin = db.Column(db.Boolean, unique=False, nullable=False)

    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.username)

    @staticmethod
    def add(username, password, admin):
        user = User(username=username, password=password, admin=admin)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    title = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=True)  # пусть текст можно будет оставить пустым
    age = db.Column(db.Integer, unique=False, nullable=True)
    info = db.Column(db.String(1000), unique=False, nullable=True)
    ispublic = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('character_list', lazy=True))
    # ссылка на модель (класс) выше
    # для User возвращает список его новостей по .user_character

    def __repr__(self):
        return '<Character {} {} {}>'.format(self.id, self.title, self.user_id)

    @staticmethod
    def add(name, title, city, age, info, ispublic, user):
        character = Character(name=name, title=title, city=city, age=age, info=info, ispublic=ispublic, user=user)
        db.session.add(character)
        db.session.commit()
        return character

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_who = db.Column(db.String(80), unique=False, nullable=False)
    to = db.Column(db.String(80), unique=False, nullable=False)
    message = db.Column(db.String(1000), unique=False, nullable=True)
    new = db.Column(db.Boolean, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return '<Message {} {} {}>'.format(self.id, self.message, self.user_id)

    @staticmethod
    def add(from_who, to, message, user):
        message = Post(from_who=from_who, to=to, message=message, new=True, user=user)
        db.session.add(message)
        db.session.commit()
        return message

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()

