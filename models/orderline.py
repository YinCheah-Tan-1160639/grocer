from . import db

class OrderLine(db.Model):
    """! The class representing an orderline object."""
    __tablename__ = 'orderline'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    # _item_id = db.Column(db.Integer, db.ForeignKey("item.id"))  # Foreign key to Item
    # Declare relationship with item and order
    item = db.relationship('Item', back_populates='orderline', uselist = False)
    order = db.relationship('Order', back_populates='orderlines')

    @property
    def order_id(self) -> int:
        """! Method to get the order id that the orderline belongs to.

        @return The order id as an integer.
        """
        return self._order_id
    
    # @property
    # def item_id(self) -> int:
    #     """! Method to get the item id that the orderline contains.

    #     @return The item id as an integer.
    #     """
    #     return self._item_id