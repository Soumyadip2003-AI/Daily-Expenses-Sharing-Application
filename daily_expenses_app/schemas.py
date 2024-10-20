from marshmallow import Schema, fields, validates, ValidationError

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    mobile = fields.Str(required=True)

class ExpenseSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Float(required=True)
    split_method = fields.Str(required=True)
    user_id = fields.Int(required=True)
    participants = fields.List(fields.Dict())

    @validates('split_method')
    def validate_split_method(self, value):
        if value not in ['equal', 'exact', 'percentage']:
            raise ValidationError("Invalid split method")

class ParticipantSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    amount_owed = fields.Float(required=True)
    percentage = fields.Float()
    expense_id = fields.Int(required=True)
