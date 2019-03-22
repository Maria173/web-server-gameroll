
from api.news_api import *


def init(app, auth):
    api = Api(app)
    api.add_resource(CharactersListApi, '/api/v1/characters', resource_class_args=[auth])
    api.add_resource(CharactersApi, '/api/v1/characters/<int:id>', resource_class_args=[auth])
