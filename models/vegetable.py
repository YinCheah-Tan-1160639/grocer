import re
from . import db, Item
from decimal import Decimal

class Vegetable(Item):
    """! The class representing a Vegetable object."""
    __tablename__ = 'vegetable'

    id: int = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    _name: str = db.Column(db.String(255), nullable=False)
    # category: str = db.Column(db.String(50), nullable=False) # ie., "Leafy green", "root vegetables", "seasonal specials", "herbs and aromatics"

    __mapper_args__ = {
        'polymorphic_identity': 'vegetable',
    }

#     # Relationship with premade boxes through the association table
#     premade_boxes: "PremadeBox" = db.relationship(
#         'PremadeBox', 
#         secondary=box_content,
#         back_populates='vegetable'
#     )

    @property
    def name(self) -> str:
        """! Method to get the vegetable name.

        @return The name of the vegetable as an string.
        """
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """! Method to set new name for the vegetable.

        @param new_name The new name to set.
        """
        self._name = new_name

#     @property
#     def category(self) -> str:
#         """! Method to get the category of the vegetable.

#         @return The category as a string.
#         """
#         pass

#     @category.setter
#     def category(self, new_category: str) -> None:
#         """! Method to set new category for the vegetable.
        
#         @param new_category The new category to set.
#         """
#         pass

    def __str__(self) -> str:
        """! The string representation of the Vegetable object.
        
        @return The Vegetable object as a string.
        """
        return f"Vegetable: {self.name}"