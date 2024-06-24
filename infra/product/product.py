from infra.database import db


class Product(db.Model):
    prd_Id = db.Column(db.Integer, primary_key = True)
    prd_Name = db.Column(db.String(50), unique = True, nullable = False)
    prd_Unit = db.Column(db.String(4), nullable = False) # jednostka miary
    prd_PriceNet = db.Column(db.Float(), nullable = False)
    prd_Ean = db.Column(db.BigInteger, nullable = True)

