from . import db, Item

class Vegetable(Item):
    """! The class representing a Vegetable object."""
    __tablename__ = 'vegetable'

    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True, autoincrement=True)
    _name = db.Column(db.String(255), nullable=False)
    _premadebox_id = db.Column(db.Integer, db.ForeignKey('premadebox.id'), nullable=True)
    # category = db.Column(db.String(50), nullable=False) # ie., "Leafy green", "root vegetables", "seasonal specials", "herbs and aromatics"
    # Relationship with premade boxes
    premadebox = db.relationship('PremadeBox', back_populates='vegetables', foreign_keys=[_premadebox_id])

    __mapper_args__ = {
        'polymorphic_identity': 'vegetable',
    }

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

    @property
    def premadebox_id(self) -> int:
        """! Method to get the premadebox id.

        @return The premadebox id as an integer.
        """
        return self._premadebox_id

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