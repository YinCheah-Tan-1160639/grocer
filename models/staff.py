from . import db, Person

class Staff(Person):
    """! The class representing an staff.
    This class inherits from the Person class.
    """

    __tablename__ = 'staff'

    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True, autoincrement=True)
    position = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    date_joined = db.Column(db.Date, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }

    def __str__(self) -> str:
        """! The string representation of the staff object.
        
        @return The staff object as a string.
        """
        return f"<Name: {self.fullname()}, Role: Staff>"