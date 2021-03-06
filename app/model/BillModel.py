from marshmallow import fields
from . import ma, types


class BillModel(object):
    def __init__(self, taxes_model):
        self.taxes_model = taxes_model
        self.price_sub_total = 0
        self.tax_sub_total = 0
        self.grand_total = 0
        self.detail = []

    def get_bill(self):
        for tax_model in self.taxes_model:
            self.add_tax(tax_model)
        return {
            'price_sub_total': self.price_sub_total,
            'tax_sub_total': self.tax_sub_total,
            'grand_total': self.grand_total,
            'detail': self.detail
        }

    def add_tax(self, tax_model):
        price = tax_model.price
        tax = tax_model.get_tax_number()
        amount = price + tax

        self.detail.append({
            'name': tax_model.name,
            'tax_code': tax_model.tax_code,
            'tax_type': types[tax_model.tax_code],
            'is_refundable': tax_model.is_refundable(),
            'price': price,
            'tax': tax,
            'amount': amount
        })

        self.price_sub_total += price
        self.tax_sub_total += tax
        self.grand_total += amount


class DetailBillSchema(ma.Schema):
    class Meta:
        fields = ('name', 'tax_code', 'tax_type', 'is_refundable', 'price', 'tax', 'amount')
    name = fields.Str(required=True)
    tax_code = fields.Int(required=True)
    tax_type = fields.Str(required=True)
    price = fields.Float(required=True)
    is_refundable = fields.Str(required=True)
    tax = fields.Float(required=True)
    amount = fields.Float(required=True)


class BillSchema(ma.Schema):
    class Meta:
        fields = ('price_sub_total', 'tax_sub_total', 'grand_total', 'detail')
    price_sub_total = fields.Float(required=True)
    tax_sub_total = fields.Float(required=True)
    grand_total = fields.Float(required=True)
    detail = fields.List(fields.Nested(DetailBillSchema(many=True)))
