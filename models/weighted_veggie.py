from . import db, Vegetable
# from .vegetable import Vegetable
from decimal import Decimal

class WeightedVeggie(Vegetable):
    """! The class representing a vegetable that is sold by weight.
    This class inherits from Vegetable.
    """
    
    __tablename__ = 'weighted_veggie'

    id = db.Column(db.Integer, db.ForeignKey('vegetable.id'), primary_key=True, autoincrement=True)
    price_per_kg = db.Column(db.Numeric(6, 2), nullable=False)
    weight = db.Column(db.Numeric(6, 2), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'weighted_veggie',
    }

    def price_display(self) -> str:
        """! Return the price display of the vegetable. Example: $15.00 per kg.
        
        @return A string representing the price per kilogram.
        """
        return f"${self.price_per_kg:.2f} per kg"

    def calculate_subtotal(self) -> Decimal:
        """! Calculate subtotal for the weighted veggie ordered.
        
        @return The subtotal of the item line.
        """
        return self.weight * self.price_per_kg

    def __str__(self) -> str:
        """! To get the string representation of the VegetableByWeight object.
        
        @return The VegetableByWeight object as a string including name and price.
        """
        return f"{super().__str__()}, Price: {self.price_display()}, Subtotal: ${self.calculate_subtotal():.2f}"
    
    
    # @property
    # def price_per_kg(self) -> Decimal:
    #     """! Method to get the price per kilogram of the vegetable.

    #     @return The price per kilogram as a Decimal.
    #     """
    #     return self._price_per_kg

    # @price_per_kg.setter
    # def price_per_kg(self, new_price: Decimal) -> None:
    #     """! Method to set new price per kilogram for the vegetable.
        
    #     @param new_price The new price per kilogram to set.
    #     """
    #     self._price_per_kg = new_price

    # @property
    # def weight(self) -> Decimal:
    #     """! Method to get the weight of the vegetable.

    #     @return The weight a Decimal.
    #     """
    #     return self._weight

    # @weight.setter
    # def weight(self, new_weight: Decimal) -> None:
    #     """! Method to set new weight for the vegetable.
        
    #     @param new_weight The new weight to set.
    #     """
    #     self._weight = new_weight