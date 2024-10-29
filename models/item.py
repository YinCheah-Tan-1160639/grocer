from . import db

class Item(db.Model):
    """! The class representing an item."""
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    _type = db.Column(db.String(50))  # 'vegetable', 'premade_box'
    _orderline_id = db.Column(db.Integer, db.ForeignKey("orderline.id"))

    # Declare relationship
    orderline = db.relationship('OrderLine', back_populates='item')

    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': _type
    }

    @property
    def type(self) -> str:
        """! Method to get the item's type.

        @return The type as a string.
        """
        return self._type
    
    @property
    def orderline_id(self) -> int:
        """! Method to get the orderline id.

        @return The orderline id as an integer.
        """
        return self._orderline_id


# # Association table used to define many-to-many relationship
# box_content = db.Table("box_content", 
#     db.Column("vegetable_id", db.Integer, db.ForeignKey('vegetable.id'), primary_key=True), 
#     db.Column("premade_box_id",db.Integer, db.ForeignKey('premade_box.id'), primary_key=True)
# )