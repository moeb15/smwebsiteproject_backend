from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    get_jwt_identity, 
    jwt_required,
    get_jwt)
from flask import request
from http import HTTPStatus
from flask_restful import Resource

from models.users import User
from utils import verify_password

blocklist = set()


class TokenResource(Resource):
    def post(self):
        json_data = request.get_json()
        email = json_data['email']
        password = json_data['password']

        user = User.get_by_email(email)

        if not user or not verify_password(password,user.password):
            return {'message':'Invalid credentials'}, HTTPStatus.FORBIDDEN

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return {'access_token':access_token, 'refresh_token':refresh_token}, HTTPStatus.OK
    
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def get(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id,fresh=False)
        return {'access_token':access_token}, HTTPStatus.OK

class RevokeResource(Resource):
    @jwt_required(optional=False)
    def post(self):
        jti = get_jwt()['jti']
        blocklist.add(jti)

        return {'message':'Successfully logged out'}, HTTPStatus.OK