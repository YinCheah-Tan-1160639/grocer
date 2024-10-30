from . import db, Vegetable
# from .vegetable import Vegetable
from decimal import Decimal

class PackVeggie(Vegetable):
    """! The class representing a vegetable that is sold in packet.
    This class inherits from Vegetable.
    """
    
    __tablename__ = 'pack_veggie'

    id = db.Column(db.Integer, db.ForeignKey('vegetable.id'), primary_key=True, autoincrement=True)
    price_per_pack = db.Column(db.Numeric(6, 2), nullable=False)
    no_of_pack = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'pack_veggie',
    }

    def price_display(self) -> str:
        """! Return the price display of the vegetable. Example: $15.00 per bag of 50g.
        
        @return A string representing the price per packet.
        """
        return f"${self.price_per_pack:.2f} per pack"
    
    def calculate_subtotal(self) -> Decimal:
        """! Calculate subtotal for the pack veggie ordered.
        
        @return The subtotal of the item line.
        """
        return self.no_of_pack * self.price_per_pack

    def __str__(self) -> str:
        """! To get the string representation of the VegetableByPack object.
        
        @return The VegetableByPack object as a string including name and price.
        """
        return f"{super().__str__()}, Price: {self.price_display()}, Subtotal: ${self.calculate_subtotal():.2f}"

    
#     @property
#     def packet_size(self) -> str:
#         """! Method to get the packet size of the vegetable.

#         @return The packet size as a string.
#         """
#         pass
    
#     @packet_size.setter
#     def packet_size(self, new_size: str) -> None:
#         """! Method to set new packet size for the vegetable.
        
#         @param new_measurement_unit The new measurement unit to set.
#         """
#         pass


    # @property
    # def price_per_pack(self) -> Decimal:
    #     """! Method to get the price per packet of the vegetable.

    #     @return The price per packet as a Decimal.
    #     """
    #     return self._price_per_pack

    # @price_per_pack.setter
    # def price_per_pack(self, new_price: Decimal) -> None:
    #     """! Method to set new price per packet for the vegetable.
        
    #     @param new_price The new price per packet to set.
    #     """
    #     self._price_per_pack = new_price
    
    # @property
    # def no_of_pack(self) -> int:
    #     """! Method to get the number of packet of the vegetable.

    #     @return The number of packet as an integer.
    #     """
    #     return self._no_of_pack

    # @no_of_pack.setter
    # def no_of_pack(self, new_number: int) -> None:
    #     """! Method to set new number of packet for the vegetable.
        
    #     @param new_number of packet The new number of packet to set.
    #     """
    #     self._no_of_pack = new_number
