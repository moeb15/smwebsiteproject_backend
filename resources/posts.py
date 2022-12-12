from flask import request, jsonify
from http import HTTPStatus
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from flask_apispec import marshal_with

from models.posts import Posts
from models.users import User
from schema.posts import PostsSchema

public_post_schema = PostsSchema(only=('post_content','created_at','username'))
private_post_schema = PostsSchema()
public_post_list_schema = PostsSchema(many=True,only=('post_content','created_at','username'))
private_post_list_schema = PostsSchema(many=True)



class PostResorce(Resource):
    @marshal_with(private_post_schema)
    @jwt_required(optional=False)
    def post(self):
        json_data = request.get_json()
        
        try:
            data = private_post_schema.load(data=json_data)
        except ValidationError as err:
            return {'message':'Validation errors','errors':err.messages}, HTTPStatus.BAD_REQUEST

        post = Posts(**data)
        post.user_id = get_jwt_identity()
        post.save()
        
        return {}, HTTPStatus.NO_CONTENT

class PostIdResource(Resource):
    @jwt_required(optional=False)
    def delete(self, id):        
        post = Posts.get_by_id(id)

        if post is None:
            return {'message':'No post found'}, HTTPStatus.NOT_FOUND
    
        if post.user_id != get_jwt_identity():
            return {'message':'Unauthorized action'}, HTTPStatus.FORBIDDEN
        
        post.delete()

        return {}, HTTPStatus.NO_CONTENT
    
    @marshal_with(private_post_schema)
    @jwt_required(optional=False)
    def get(self, id):
        post = Posts.get_by_id(id)

        if post is None:
            return {'message':'No post found'}, HTTPStatus.NOT_FOUND
        
        if post.user_id != get_jwt_identity():
            return public_post_schema.dump(post), HTTPStatus.OK
        

        return private_post_schema.dump(post), HTTPStatus.OK
    
    
class PostListResource(Resource):
    @jwt_required(optional=False)
    def get(self):
        posts = Posts.get_all_posts(get_jwt_identity())

        return private_post_list_schema.dump(posts),  HTTPStatus.OK
