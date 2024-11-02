from . import db, Vegetable
from decimal import Decimal

class WeightedVeggie(Vegetable):
    """! The class representing a vegetable that is sold by weight.
    This class inherits from Vegetable.
    """
    
    __tablename__ = 'weighted_veggie'

    id = db.Column(db.Integer, db.ForeignKey('vegetable.id'), primary_key=True, autoincrement=True)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    weight = db.Column(db.Numeric(6, 2), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'weighted_veggie',
    }

    def price_display(self) -> str:
        """! Return the price display of the vegetable. Example: $15.00 per kg.
        
        @return A string representing the price per kilogram.
        """
        return f"${self.price:.2f}/kg"
    
    def subtotal_display(self) -> str:
        """! Return the subtotal display of the vegetable. Example: $30.00.
        
        @return A string representing the subtotal of the item line.
        """
        return f"${self.calculate_subtotal():.2f}"
    
    def quantity_display(self) -> str:
        """! Return the quantity display of the vegetable. Example: 2 kg.
        
        @return A string representing the quantity of the item line.
        """
        return f"{self.weight} kg"

    def calculate_subtotal(self) -> Decimal:
        """! Calculate subtotal for the weighted veggie ordered.
        
        @return The subtotal of the item line.
        """
        return self.weight * self.price

    def __str__(self) -> str:
        """! To get the string representation of the VegetableByWeight object.
        
        @return The VegetableByWeight object as a string including name and price.
        """
        return f"{super().__str__()}, {self.price_display()}"