from flask import request, json, Response, Blueprint
from model.TaxModel import TaxSchema, TaxModel
from model.BillModel import BillModel, BillSchema

tax_api = Blueprint('tax_api', __name__)

bill_schema = BillSchema()
tax_schema = TaxSchema()
taxes_schema = TaxSchema(many=True)


@tax_api.route('/', methods=['POST'])
def add_tax():
    """
        Tax object creation endpoint
        ---
        tags:
          - tax
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: Tax
              required:
                - name
                - tax_code
                - price
              properties:
                name:
                  type: string
                  description: Entry name
                tax_code:
                  type: integer
                  description: Tax code (1, 2, or 3)
                price:
                  type: integer
                  description: Price of the entry
        responses:
          200:
            description: Tax object inserted in the database
            schema:
              $ref: '#/definitions/Tax'
    """
    req_data = request.get_json()
    data, error = tax_schema.load(req_data)

    if error:
        return custom_response(error, 400)

    tax = TaxModel(data)
    tax.save()

    return tax_schema.jsonify(tax)


@tax_api.route('/', methods=['GET'])
def get_all_tax():
    """
        Bill object retrieval
        ---
        tags:
          - bill
        parameters: []
        responses:
          200:
            description: Bill object is retrieved from database
            schema:
              id: Bill
              properties:
                detail:
                  type: array
                  items:
                    type: object
                    properties:
                        name:
                          type: string
                          description: Entry name
                        tax_code:
                          type: integer
                          description: Tax code (1, 2, or 3)
                        price:
                          type: integer
                          description: Price of the entry
                        tax:
                          type: integer
                          description: Tax of the entry
                        amount:
                          type: integer
                          description: Amount of the entry (Price + Tax)
                        tax_type:
                          type: string
                          description: Type of the tax
                        is_refundable:
                          type: string
                          description: Information about the entry. Is it refundable or not?
                          enum:
                          - "Yes"
                          - "No"
                grand_total:
                  type: integer
                  description: Grand total of the bill (Price + Tax)
                price_sub_total:
                  type: integer
                  description: Price sub total of the bill
                tax_sub_total:
                  type: integer
                  description: Tax sub total of the bill
    """
    all_tax = TaxModel.get_all_tax()
    bills = BillModel(all_tax)

    return bill_schema.jsonify(bills.get_bill())


def custom_response(res, status_code):
    return Response(
        mimetype='application/json',
        response=json.dumps(res),
        status=status_code
    )
