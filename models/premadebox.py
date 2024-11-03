from . import db, Item, Vegetable
from decimal import Decimal

class PremadeBox(Item):
    """! The class representing a PremadeBox object."""
    __tablename__ = 'premadebox'

    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True, autoincrement=True)
    size = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    no_of_boxes = db.Column(db.Integer, nullable=False)
    # Add relationship to vegetables associated with the premadebox
    vegetables = db.relationship('Vegetable', back_populates='premadebox', foreign_keys=[Vegetable.premadebox_id])

    __mapper_args__ = {
        'polymorphic_identity': 'premadebox'
    }

    def calculate_subtotal(self):
        """! Calculate subtotal for the number of boxes ordered.
        
        @return The subtotal of item line.
        """
        return self.price * self.no_of_boxes

    def box_content(self) -> str:
        """! Return the list of vegetables contain in the premade box.
        
        @return The list of vegetables.
        """
        return [veg.name for veg in self.vegetables]

    def price_display(self) -> str:
        """! Return the price display of the premade box. Example: $15.00 per box.
        
        @return A string representing the price per box.
        """
        return f"${self.price:.2f} per box"
    
    def quantity_display(self) -> str:
        """! Return the quantity display of the premade box. Example: 2 boxes.
        
        @return A string representing the quantity of the item line.
        """
        return f"{self.no_of_boxes} box" if self.no_of_boxes == 1 else f"{self.no_of_boxes} boxes"
    
    def get_quantity(self) -> Decimal:
        """! Get the quantity of the premade box ordered.
        
        @return The number of boxes as a Decimal.
        """
        return self.no_of_boxes
    
    def subtotal_display(self) -> str:
        """! Return the subtotal display of the premade box. Example: $30.00.
        
        @return A string representing the subtotal of the item line.
        """
        return f"${self.calculate_subtotal():.2f}"
    
    def box_name(self) -> str:
        """! Return the name of the premade box.
        
        @return The name of the premade box.
        """
        return f"{self.size} Premade Box"

    def __str__(self) -> str:
        """! To get the string representation of the Premade box object.
        
        @return The premadebox object as a string.
        """
        return f"{self.size} Premade Box"
    
    
    # @property
    # def size(self) -> str:
    #     """! Method to get the size of the premade box.

    #     @return The size as a string.
    #     """
    #     return self._size

    # @size.setter
    # def size(self, new_size: str) -> None:
    #     """! Method to set new size for the premade box.
        
    #     @param new_size The new size to set.
    #     """
    #     self._size = new_size

    # @property
    # def price(self) -> Decimal:
    #     """! Method to get the price per box.
        
    #     @return The price per box as a Decimal.
    #     """
    #     return self._price
    
    # @price.setter
    # def price(self, new_price: Decimal) -> None:
    #     """! Method to set new price per box.
        
    #     @param new_price The new price to set.
    #     """
    #     self._price = new_price
    
    # @property
    # def no_of_boxes(self) -> int:
    #     """! Method to get the number of boxes.
        
    #     @return The number of boxes as an integer.
    #     """
    #     return self._no_of_boxes
    
    # @no_of_boxes.setter
    # def no_of_boxes(self, new_no_of_boxes: int) -> None:
    #     """! Method to set new number of boxes.
        
    #     @param new_no_of_boxes The new number of boxes to set.
    #     """
    #     self._no_of_boxes = new_no_of_boxes

    
    # @classmethod
    # def update_price(cls, size: str, new_price: Decimal):
    #     """Update the price of a box size."""
    #     if size in cls.BOX_PRICES:
    #         cls.BOX_PRICES[size] = new_price
    #     else:
    #         raise ValueError("Invalid box size. Choose from 'small', 'medium', or 'large'.") 

#     def add_vegetable(self, vegetable: 'Vegetable') -> None:
#         """Add a vegetable (of any type) to the premade box."""
#         if vegetable not in self.box_content:
#             self.box_content.append(vegetable)
    
#     def remove_vegetable(self, vegetable: 'Vegetable') -> None:
#         """Remove a vegetable from the premade box."""
#         if vegetable in self.box_content:
#             self.box_content.remove(vegetable)