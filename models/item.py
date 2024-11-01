from . import db

class Item(db.Model):
    """! The class representing an item."""
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    type = db.Column(db.String(50))  # 'vegetable', 'premade_box'
    # orderline_id = db.Column(db.Integer, db.ForeignKey("orderline.id"))

    # Declare relationship
    orderline = db.relationship('OrderLine', back_populates='item', uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': type
    }