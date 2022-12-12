from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS
from flask_apispec.extension import FlaskApiSpec

from extensions import db, jwt
from config import Config
from models.users import User
from models.posts import Posts
from models.friends import Friends
from resources.users import UserResource, MeResource
from resources.token import TokenResource, RefreshResource, RevokeResource, blocklist
from resources.posts import PostResorce, PostListResource, PostIdResource
from resources.friends import AddFriendsResource, ConfirmRequestResource

from schema.posts import PostsSchema
from schema.users import UserSchema


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    regisiter_resources(app)
    
    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app,db)
    jwt.init_app(app)
    CORS(app, allow_headers='Content-type')

    @jwt.token_in_blocklist_loader
    def check_if_in_blocklist(jwt_header,jwt_payload: dict):
        jti = jwt_payload['jti']
        token_in_redis = next((elem for elem in blocklist if elem == jti),None)
        return token_in_redis in blocklist

def regisiter_resources(app):
    docs = FlaskApiSpec(app)
    api = Api(app)

    #post resources
    api.add_resource(PostResorce,'/posts')
    api.add_resource(PostListResource, '/posts/myposts')
    api.add_resource(PostIdResource, '/posts/<int:id>')
    #user resources
    api.add_resource(UserResource, '/users')
    api.add_resource(MeResource, '/me')
    api.add_resource(AddFriendsResource, '/users/<string:username>')
    api.add_resource(ConfirmRequestResource, '/users/confirm/<string:username>')
    #jwt resources
    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/token/refresh')
    api.add_resource(RevokeResource, '/token/revoke')

    #swagger docs
    #need to be worked on
    docs.register_existing_resources()

if __name__ =='__main__':
    app = create_app()
    app.run()
