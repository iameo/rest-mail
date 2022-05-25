from flask_login import UserMixin

# from marshmallow import Schema, fields

class User(UserMixin):
    '''Flask-Login requires a model in object form to login users
    is_authenticated, is_active is plugged in from the mixin
    '''
    def __init__(self, _json=None):
        ''' collect dict from mongodb'''
        self._json = _json
        
    def get_id(self):
        _id = self._json["_id"]
        return str(_id)

    def get_username(self):
        return self._json["username"]
        


# class ObjectId(fields.Field):
#     def _serialize(self, value, attr, obj, **kwargs):
#         if value is None:
#             return ""
#         return "".join(str(d) for d in value)

#     def _deserialize(self, value, attr, data, **kwargs):
#         try:
#             return [int(c) for c in value]
#         except ValueError as error:
#             raise ValidationError("Pin codes must contain only digits.") from error

# class User:
#     def __init__(self, username, full_name, dob, password) -> None:
#         self.username = username
#         self.full_name = full_name
#         self.date_of_birth = dob
#         self.password = passwor

# class UserSchema(Schema):
#     _id = ObjectId()
#     full_name = fields.String()
#     username = fields.String()
#     date_of_birth = fields.String()
#     password = fields.String()
