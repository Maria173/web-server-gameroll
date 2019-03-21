from flask_restful import Resource, Api
from flask_restful import reqparse
from flask import jsonify
from flask import abort
import extra.auth as auth
from models import Character

news_parser = reqparse.RequestParser()
news_parser.add_argument('title', required=True)
news_parser.add_argument('name', required=True)
news_parser.add_argument('city', required=True)
news_parser.add_argument('age', required=True, type=int)
news_parser.add_argument('info', required=True)
news_parser.add_argument('ispublic', required=False, type=bool)


class NewsListApi(Resource):
    def __init__(self, auth):
        super(NewsListApi, self).__init__()
        self._auth = auth

    def get(self):
        news = Character.query.all()
        return jsonify(news=[i.serialize for i in news])

    def post(self):
        if not self._auth.is_authorized():
            abort(401)
        args = news_parser.parse_args()
        print(args)
        news = Character.add(args['name'], args['title'], args['city'],
                             args['age'], args['info'], args['ispublic'], self._auth.get_user())
        return jsonify(news.serialize)


class NewsApi(Resource):

    def __init__(self, auth):
        super(NewsApi, self).__init__()
        self._auth = auth

    def get(self, id):
        news = Character.query.filter_by(id=id).first()
        if not news:
            abort(404)
        return jsonify(news.serialize)

    def delete(self, id):
        if not self._auth.is_authorized():
            abort(401)
        news = Character.query.filter_by(id=id).first()
        if news.user_id != self._auth.get_user().id:
            abort(403)
        Character.delete(news)
        return jsonify({"deleted": True})
