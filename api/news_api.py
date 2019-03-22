from flask_restful import Resource, Api
from flask_restful import reqparse
from flask import jsonify
from flask import abort
import extra.auth as auth
from models import Character

characters_parser = reqparse.RequestParser()
characters_parser.add_argument('title', required=True)
characters_parser.add_argument('name', required=True)
characters_parser.add_argument('city', required=True)
characters_parser.add_argument('age', required=True, type=int)
characters_parser.add_argument('info', required=True)
characters_parser.add_argument('ispublic', required=False, type=bool)


class CharactersListApi(Resource):
    def __init__(self, auth):
        super(CharactersListApi, self).__init__()
        self._auth = auth

    def get(self):
        characters = Character.query.all()
        return jsonify(characters=[i.serialize for i in characters])

    def post(self):
        if not self._auth.is_authorized():
            abort(401)
        args = characters_parser.parse_args()
        characters = Character.add(args['name'], args['title'], args['city'],
                             args['age'], args['info'], args['ispublic'], self._auth.get_user())
        return jsonify(characters.serialize)


class CharactersApi(Resource):

    def __init__(self, auth):
        super(CharactersApi, self).__init__()
        self._auth = auth

    def get(self, id):
        characters = Character.query.filter_by(id=id).first()
        if not characters:
            abort(404)
        return jsonify(characters.serialize)

    def delete(self, id):
        if not self._auth.is_authorized():
            abort(401)
        characters = Character.query.filter_by(id=id).first()
        if characters.user_id != self._auth.get_user().id:
            abort(403)
        Character.delete(characters)
        return jsonify({"deleted": True})
