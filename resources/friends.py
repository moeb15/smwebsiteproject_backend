from flask import request
from http import HTTPStatus
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from models.friends import Friends
from models.users import User


class AddFriendsResource(Resource):
    @jwt_required(optional=False)
    def post(self, username):
        receiver = User.get_by_username(username)

        if receiver is None:
            return {'message': 'No user found'}, HTTPStatus.NOT_FOUND

        if receiver.id == get_jwt_identity():
            return {'message':'Cannot send requests to yourself'}, HTTPStatus.BAD_REQUEST

        f_request = Friends.get_friend_request(user_id=get_jwt_identity(), recipient=receiver.id)
        
        if f_request != None:
            if f_request.is_added == True:
                return {'message':'Already in friends list'}, HTTPStatus.BAD_REQUEST
            elif f_request.is_added == False:
                return {'message': 'Friend request already sent'}, HTTPStatus.BAD_REQUEST

        friend_request = Friends()
        friend_request.user_id = get_jwt_identity()
        friend_request.recipient = receiver.id
        friend_request.save()

        return {'message': f'Friend request sent to {receiver.username}'}, HTTPStatus.OK


class ConfirmRequestResource(Resource):
    @jwt_required(optional=False)
    def post(self, username):
        user = User.get_by_id(get_jwt_identity())
        sender = User.get_by_username(username)

        if sender is None:
            return {'message': 'User not found'}, HTTPStatus.BAD_REQUEST

        friend_request = Friends.get_friend_request(
            user_id=sender.id, recipient=user.id)

        if friend_request is None:
            return {'message': 'Request not found'}, HTTPStatus.BAD_REQUEST

        if friend_request.is_added is True:
            return {'message': 'Already in friends list'}, HTTPStatus.BAD_REQUEST

        friend_request.is_added = True
        friend_request.save()

        return {'message': f'Friend request from {sender.username} confirmed'}, HTTPStatus.OK

    @jwt_required(optional=False)
    def delete(self, username):
        user = User.get_by_id(get_jwt_identity())
        sender = User.get_by_username(username)

        if sender is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        friend_request = Friends.get_friend_request(
            user_id=sender.id, recipient=user.id)

        if friend_request is None:
            return {'message': 'No request or friend found'}, HTTPStatus.BAD_REQUEST

        if friend_request.is_added == True:
            friend_request.delete()
            return {'message': 'Friend removed'}, HTTPStatus.OK

        friend_request.delete()

        return {'message': 'Request removed'}, HTTPStatus.OK
