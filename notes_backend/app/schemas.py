from marshmallow import Schema, fields, validate

# PUBLIC_INTERFACE
class UserSchema(Schema):
    """Schema for user output."""
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    created_at = fields.DateTime(dump_only=True)

# PUBLIC_INTERFACE
class UserRegisterSchema(Schema):
    """Schema for user registration (input)."""
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6, max=128))

# PUBLIC_INTERFACE
class UserLoginSchema(Schema):
    """Schema for user login (input)."""
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

# PUBLIC_INTERFACE
class NoteSchema(Schema):
    """Schema for note output/input."""
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    content = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
