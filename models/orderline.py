from . import db

class OrderLine(db.Model):
    """! The class representing an orderline object."""
    __tablename__ = 'orderline'

    id = db.Column(db.Integer, primary_key=True)
    _order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    # Declare relationship with item and order
    item = db.relationship('Item', backpopulates='orderline')
    order = db.relationship('Order', backpopulates='orderlines')