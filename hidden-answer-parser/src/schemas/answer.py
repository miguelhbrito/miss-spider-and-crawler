from marshmallow import Schema, fields

from src.schemas.comment import CommentSchema
from src.schemas.user import UserSchema


class AnswerSchema(Schema):
    up_votes = fields.Int()
    down_votes = fields.Int()
    content = fields.Str()
    created_at = fields.DateTime()
    user = fields.Nested(UserSchema)
    comments = fields.List(fields.Nested(CommentSchema))
