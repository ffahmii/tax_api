from flask import request, Blueprint, jsonify
from model.TaxModel import TaxSchema, TaxModel

tax_api = Blueprint('tax_api', __name__)

tax_schema = TaxSchema()


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
          400:
            description: Invalid input from user
    """
    req_data = request.get_json()
    data, error = tax_schema.load(req_data)

    if error:
        return jsonify(error), 400

    try:
        tax = TaxModel(data)
        tax.save()

        return tax_schema.jsonify(tax)
    except AssertionError as exception:
        error = exception.message
        return jsonify({error['field']: [error['message']]}), 400
