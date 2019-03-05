from flask import request, json, Response, Blueprint
from model.TaxModel import TaxSchema, TaxModel
from model.BillModel import BillModel, BillSchema

tax_api = Blueprint('tax_api', __name__)

bill_schema = BillSchema()
tax_schema = TaxSchema()
taxes_schema = TaxSchema(many=True)


@tax_api.route('/', methods=['POST'])
def add_tax():
    req_data = request.get_json()
    data, error = tax_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    tax = TaxModel(data)
    tax.save()

    return tax_schema.jsonify(tax)


@tax_api.route('/', methods=['GET'])
def get_all_tax():
    all_tax = TaxModel.get_all_tax()
    bills = BillModel(all_tax)

    return bill_schema.jsonify(bills.get_bill())


def custom_response(res, status_code):
    return Response(
        mimetype='application/json',
        response=json.dumps(res),
        status=status_code
    )
