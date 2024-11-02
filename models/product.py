from . import db

class Product(db.Model):
    """! The class representing a product."""
    
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    available = db.Column(db.Boolean, nullable=False, default=True)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'product',
        'polymorphic_on': 'type',
    }

class VegetableProduct(Product):
    """! The class representing a vegetable product."""
    __tablename__ = 'vegetable_product'

    id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    unit = db.Column(db.String(20), nullable=False) # 'kg', 'unit', 'pack'

    __mapper_args__ = {
        'polymorphic_identity': 'vegetable',
    }

class PremadeBoxProduct(Product):
    """! The class representing a premade box product."""
    __tablename__ = 'premade_box_product'

    id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    size = db.Column(db.String(20), nullable=False) # 'small', 'medium', 'large'
    price = db.Column(db.Numeric(6, 2), nullable=False)

    # Declare relationship with BoxComponent
    components = db.relationship('BoxComponent', back_populates='box')

    __mapper_args__ = {
        'polymorphic_identity': 'premade_box',
    }
    
class BoxComponent(db.Model):
    """! A model representing a component in a premade box."""
    __tablename__ = 'box_component'

    id = db.Column(db.Integer, primary_key=True)
    box_id = db.Column(db.Integer, db.ForeignKey('premade_box_product.id'))
    vegetable_id = db.Column(db.Integer, db.ForeignKey('vegetable_product.id'))
    quantity = db.Column(db.Numeric(10, 2), nullable=False)  # Quantity of the vegetable in the box

    # Declare relationships
    box = db.relationship('PremadeBoxProduct', back_populates='components')
    vegetable = db.relationship('VegetableProduct')