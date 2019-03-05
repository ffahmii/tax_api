from marshmallow import fields
from . import db, ma


class TaxModel(db.Model):
    __tablename__ = 'tax'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    tax_code = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, data):
        self.name = data.get('name')
        self.tax_code = data.get('tax_code')
        self.price = data.get('price')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
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
            return True
        elif self.tax_code == 2:
            return False
        elif self.tax_code == 3:
            return False
        else:
            return False

    @staticmethod
    def get_all_tax():
        return TaxModel.query.all()

    def __repr(self):
        return '<id {}>'.format(self.id)


class TaxSchema(ma.Schema):
    class Meta:
        fields = ('name', 'tax_code', 'price')
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    tax_code = fields.Int(required=True)
    price = fields.Int(required=True)
