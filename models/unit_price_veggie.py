from . import db, Vegetable
from decimal import Decimal

class UnitPriceVeggie(Vegetable):
    """! The class representing a vegetable that is sold by unit.
    This class inherits from Vegetable.
    """
    
    __tablename__ = 'unit_price_veggie'

    id = db.Column(db.Integer, db.ForeignKey('vegetable.id'), primary_key=True, autoincrement=True)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'unit_price_veggie',
    }

    def price_display(self) -> str:
        """! Return the price display of the vegetable. Example: $15.00 per each.
        
        @return A string representing the price per unit of measurement.
        """
        return f"${self.price:.2f}/each"

    def calculate_subtotal(self) -> Decimal:
        """! Calculate subtotal for the unit price veggie ordered.
        
        @return The subtotal of the item line.
        """
        return self.quantity * self.price

    def __str__(self) -> str:
        """! To get the string representation of the VegetableByUnit object.
        
        @return The VegetableByUnit object as a string including name and price.
        """
        return f"{super().__str__()}, Price: {self.price_display()}"