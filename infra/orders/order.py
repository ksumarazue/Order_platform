from infra.database import db


class Order(db.Model):
    ord_id = db.Column(db.Integer, primary_key = True)
    ord_UsrId = db.Column(db.Integer, nullable = False)
    ord_UsrName = db.Column(db.String(20), nullable = False)
    ord_Status = db.Column(db.String(20), nullable = False)


class OrderElements(db.Model):
    ordEl_id = db.Column(db.Integer, primary_key = True)
    ordEl_OrdId = db.Column(db.Integer, nullable = False)
    ordEl_ProdId = db.Column(db.Integer, nullable = False)
    ordEl_ProdName = db.Column(db.String(50), nullable = False)
    ordEl_ProdUnit = db.Column(db.String(4), nullable = False) # jednostka miary
    ordEl_Quantity = db.Column(db.Integer, nullable = False)
    ordEl_ProdPriceNet = db.Column(db.Float(), nullable = False)
    ordEl_ProdPriceSum = db.Column(db.Float(), nullable = False)





