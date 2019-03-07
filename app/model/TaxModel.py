from marshmallow import fields
from . import db, ma
from sqlalchemy.orm import validates


class TaxModel(db.Model):
    __tablename__ = 'tax'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    tax_code = db.Column(db.Integer, nullable=False)

    def __init__(self, data):
        self.name = data.get('name')
        self.tax_code = data.get('tax_code')
        self.price = data.get('price')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_tax_number(self):
        if self.tax_code == 1:
            return 0.1 * self.price
        elif self.tax_code == 2:
            return 10 + (0.02 * self.price)
        elif self.tax_code == 3:
            if self.price < 100 & self.price > 0:
                return 0
            else:
                return 0.01 * (self.price - 100)
        else:
            return 0

    def is_refundable(self):
        if self.tax_code == 1:
            return "Yes"
        elif self.tax_code == 2:
            return "No"
        elif self.tax_code == 3:
            return "No"
        else:
            return "No"

    @staticmethod
    def get_all_tax():
        return TaxModel.query.all()

    def __repr(self):
        return '<id {}>'.format(self.id)

    @validates('tax_code')
    def validate_tax_code(self, key, value):
        if value not in [1, 2, 3]:
            raise AssertionError({
                'field': 'tax_code',
                'message': 'Tax code is invalid. Tax code should be 1, 2, or 3'
            })

        return value


class TaxSchema(ma.Schema):
    class Meta:
        fields = ('name', 'tax_code', 'price')

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    tax_code = fields.Int(required=True)
    price = fields.Int(required=True)
