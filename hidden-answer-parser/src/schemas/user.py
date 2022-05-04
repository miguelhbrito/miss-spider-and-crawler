from marshmallow import Schema, fields

class UserSchema(Schema):
    name = fields.Str()
    title = fields.Str()
    score = fields.Int()
