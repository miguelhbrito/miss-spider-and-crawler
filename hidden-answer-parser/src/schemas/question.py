from marshmallow import Schema, fields

from src.schemas.answer import AnswerSchema
from src.schemas.comment import CommentSchema
from src.schemas.user import UserSchema


class QuestionSchema(Schema):
    up_votes = fields.Int()
    down_votes = fields.Int()
    title = fields.Str()
    content = fields.Str()
    tags = fields.List(fields.Str())
    category = fields.Str()
    author = fields.Nested(UserSchema)
    created_at = fields.DateTime()
    best_answer = fields.Nested(AnswerSchema)
    comments = fields.List(fields.Nested(CommentSchema))
    answers = fields.List(fields.Nested(AnswerSchema))
