from . import db, Item

class Vegetable(Item):
    """! The class representing a Vegetable object."""
    __tablename__ = 'vegetable'

    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    premadebox_id = db.Column(db.Integer, db.ForeignKey('premadebox.id'), nullable=True)
    # Relationship with premade boxes
    premadebox = db.relationship('PremadeBox', back_populates='vegetables', foreign_keys=[premadebox_id])

    __mapper_args__ = {
        'polymorphic_identity': 'vegetable',
    }

    def __str__(self) -> str:
        """! The string representation of the Vegetable object.
        
        @return The Vegetable object as a string.
        """
        return f"Vegetable: {self.name}"