from marshmallow_sqlalchemy import auto_field, SQLAlchemyAutoSchema
from marshmallow import fields, validates_schema, validates, ValidationError

from models import UserModel


class LoginUserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

    id = auto_field(load_only=True)
    email = fields.Email(
        required=True, error_messages={"required": "you must include an 'email' field"}
    )
    password = auto_field(
        required=True,
        error_messages={"required": "you must include a 'password' field"},
    )

    @validates("password")
    def password_validation(self, password):
        if len(password) < 6:
            raise ValidationError("Password is too short.")


class RegisterUserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

    id = auto_field(load_only=True)
    email = fields.Email(
        required=True, error_messages={"required": "you must include an 'email' field"}
    )
    username = auto_field(
        required=True,
        error_messages={"required": "you must include a 'username' field"},
    )
    password1 = fields.String(
        required=True,
        error_messages={"required": "you must include a 'password1' field"},
    )
    password2 = fields.String(
        required=True,
        error_messages={"required": "you must include a 'password2' field"},
    )

    @validates("email")
    def email_validation(self, email):
        if UserModel.get_by_email(email):
            raise ValidationError("Email is already in use.")

    @validates("username")
    def username_validation(self, username):
        if UserModel.get_by_username(username):
            raise ValidationError("Username is already in use")
        if (len(username) < 3) or (len(username) > 50):
            raise ValidationError("Username must be between 3 and 50 characters")

    @validates("password1")
    def password_validation(self, password):
        # TODO do more complex password validation here like checking complexity
        if len(password) < 6:
            raise ValidationError("Password is too short.")

    @validates_schema
    def passwords_match(self, data, **kwargs):
        if data["password1"] != data["password2"]:
            raise ValidationError("Passwords don't match!")
