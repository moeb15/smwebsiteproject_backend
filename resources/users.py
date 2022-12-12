from flask import request
from http import HTTPStatus
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from models.users import User
from schema.users import UserSchema
from utils import hash_password

user_schema = UserSchema()

class UserResource(Resource):
    def post(self):
        json_data = request.get_json()

        try:
            data = user_schema.load(data=json_data)
        except ValidationError as err:
            return {'message':'Validation error', 'errors':err.messages}, HTTPStatus.BAD_REQUEST

        username = json_data['username']
        email = json_data['email']

        if User.get_by_username(username) != None:
            return {'message': 'Username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(email) != None:
            return {'message': 'Email already used'}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()
        
        return {'message':'Account created'}, HTTPStatus.CREATED

class MeResource(Resource):
    @jwt_required(optional=False)
    def get(self):
        json_data = request.get_json()
        user = User.get_by_email(json_data['email'])

        if not user:
            return {'message':'No user found'}, HTTPStatus.NOT_FOUND
        
        if user.id != get_jwt_identity():
            return {'message':'Unauthorized action'}, HTTPStatus.FORBIDDEN

        return user_schema.dump(user), HTTPStatus.OK

        
