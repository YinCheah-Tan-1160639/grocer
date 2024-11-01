from . import db

class OrderLine(db.Model):
    """! The class representing an orderline object."""
    __tablename__ = 'orderline'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))

    # Declare relationship with item and order
    item = db.relationship('Item', back_populates='orderline')
    order = db.relationship('Order', back_populates='orderlines')