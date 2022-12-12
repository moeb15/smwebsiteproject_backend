from marshmallow import fields, Schema, validate
from utils import hash_password

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username= fields.Str(required=True,validate=[validate.Length(min=3,max=100)])
    password = fields.Method(deserialize='load_password')
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)
    
    def load_password(self,password):
        return hash_password(password)