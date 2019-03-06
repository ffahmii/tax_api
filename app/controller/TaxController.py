from flask import request, json, Response, Blueprint
from model.TaxModel import TaxSchema, TaxModel

tax_api = Blueprint('tax_api', __name__)

tax_schema = TaxSchema()
taxes_schema = TaxSchema(many=True)


@tax_api.route('/', methods=['POST'])
def post():
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
        return Response(
            mimetype='application/json',
            response=json.dumps(error),
            status=400
        )

    tax = TaxModel(data)
    tax.save()

    return tax_schema.jsonify(tax)
