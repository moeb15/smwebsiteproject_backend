from flask import request, jsonify
from http import HTTPStatus
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError, fields
from webargs.flaskparser import use_kwargs

from models.posts import Posts
from models.users import User
from schema.posts import PostsSchema
from schema.pagination import PostsPaginationSchema

post_schema = PostsSchema()
post_list_schema = PostsPaginationSchema()



class PostResorce(Resource):
    @jwt_required(optional=False)
    def post(self):
        json_data = request.get_json()
        
        try:
            data = post_schema.load(data=json_data)
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
    
    
    @jwt_required(optional=False)
    def get(self, id):
        post = Posts.get_by_id(id)

        if post is None:
            return {'message':'No post found'}, HTTPStatus.NOT_FOUND
        

        return post_schema.dump(post), HTTPStatus.OK
    
    
class PostListResource(Resource):
    @use_kwargs({'page':fields.Int(missing=1),
                'per_page':fields.Int(missing=20)}, location='query')
    @jwt_required(optional=False)
    def get(self, page, per_page):
        posts = Posts.get_all_posts(get_jwt_identity(),page,per_page)

        return post_list_schema.dump(posts),  HTTPStatus.OK
