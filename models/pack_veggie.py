from . import db, Vegetable
from decimal import Decimal

class PackVeggie(Vegetable):
    """! The class representing a vegetable that is sold in packet.
    This class inherits from Vegetable.
    """
    
    __tablename__ = 'pack_veggie'

    id = db.Column(db.Integer, db.ForeignKey('vegetable.id'), primary_key=True, autoincrement=True)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    no_of_pack = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'pack_veggie',
    }

    def price_display(self) -> str:
        """! Return the price display of the vegetable. Example: $15.00 per bag of 50g.
        
        @return A string representing the price per packet.
        """
        return f"${self.price:.2f}/pack"
    
    def calculate_subtotal(self) -> Decimal:
        """! Calculate subtotal for the pack veggie ordered.
        
        @return The subtotal of the item line.
        """
        return self.no_of_pack * self.price

    def __str__(self) -> str:
        """! To get the string representation of the VegetableByPack object.
        
        @return The VegetableByPack object as a string including name and price.
        """
        return f"{super().__str__()}, Price: {self.price_display()}"