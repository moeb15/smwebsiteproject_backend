from marshmallow import fields, Schema, validate
from schema.users import UserSchema

class PostsSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id=fields.Int(dump_only=True)
    post_content= fields.Str(required=True,validate=[validate.Length(min=1,max=300)])
    username = fields.Nested(UserSchema(only=('username',)))
    created_at = fields.DateTime(dump_only=True)

