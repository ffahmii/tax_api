from flask import request, json, Response, Blueprint
from model.BillModel import BillModel, BillSchema
from model.TaxModel import TaxModel

bill_api = Blueprint('bill_api', __name__)

bill_schema = BillSchema()


@bill_api.route('/', methods=['GET'])
def get():
    """
        Bill object retrieval endpoint
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
