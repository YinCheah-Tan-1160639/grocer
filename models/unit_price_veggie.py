from . import db, Vegetable
# from .vegetable import Vegetable
from decimal import Decimal

class UnitPriceVeggie(Vegetable):
    """! The class representing a vegetable that is sold by unit.
    This class inherits from Vegetable.
    """
    
    __tablename__ = 'unit_price_veggie'

    id = db.Column(db.Integer, db.ForeignKey('vegetable.id'), primary_key=True, autoincrement=True)
    price_per_unit = db.Column(db.Numeric(6, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'unit_price_veggie',
    }

    def price_display(self) -> str:
        """! Return the price display of the vegetable. Example: $15.00 per each.
        
        @return A string representing the price per unit of measurement.
        """
        return f"${self.price_per_unit:.2f} per each"

    def calculate_subtotal(self) -> Decimal:
        """! Calculate subtotal for the unit price veggie ordered.
        
        @return The subtotal of the item line.
        """
        return self.quantity * self.price_per_unit

    def __str__(self) -> str:
        """! To get the string representation of the VegetableByUnit object.
        
        @return The VegetableByUnit object as a string including name and price.
        """
        return f"{super().__str__()}, Price: {self.price_display()}, Subtotal: ${self.calculate_subtotal():.2f}"
    
    # _measurement_unit: str = db.Column(db.String(100), default='each', nullable=False)
        
#     @property
#     def measurement_unit(self) -> str:
#         """! Method to get the measurement unit of the vegetable.

#         @return The measurement unit as a string.
#         """
#         pass

#     @measurement_unit.setter
#     def measurement_unit(self, new_measurement_unit) -> None:
#         """! Method to set new unit of measurement for the vegetable.
        
#         @param new_measurement_unit The new measurement unit to set.
#         """
#         pass

    # @property
    # def price_per_unit(self) -> Decimal:
    #     """! Method to get the price per unit of the vegetable.

    #     @return The price per unit as a Decimal.
    #     """
    #     return self._price_per_unit

    # @price_per_unit.setter
    # def price_per_unit(self, new_price: Decimal) -> None:
    #     """! Method to set new price per unit for the vegetable.
        
    #     @param new_price The new price per unit to set.
    #     """
    #     self._price_per_unit = new_price

    # @property
    # def quantity(self) -> int:
    #     """! Method to get the quantity of the vegetable.

    #     @return The quantity as an integer.
    #     """
    #     return self._quantity
    
    # @quantity.setter
    # def quantity(self, new_quantity: int) -> None:
    #     """! Method to set new quantity for the vegetable.
        
    #     @param new_quantity The new quantity to set.
    #     """
    #     self._quantity = new_quantity

    