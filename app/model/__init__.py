from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

from TaxModel import TaxModel, TaxSchema
from TaxType import types
from BillModel import BillModel, BillSchema
