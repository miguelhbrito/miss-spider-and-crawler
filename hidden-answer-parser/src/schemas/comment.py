from marshmallow import Schema, fields
from src.schemas.user import UserSchema


class CommentSchema(Schema):
    content = fields.Str()
    created_at = fields.DateTime()
    author = fields.Nested(UserSchema)
