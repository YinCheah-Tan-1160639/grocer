from . import db
from sqlalchemy.sql import func
# from datetime import datetime
from . import hashing

class Person(db.Model):
    """! The class representing a person."""

    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    family_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)    
    username = db.Column(db.String(30), unique=True, nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    type = db.Column(db.String(50)) # Discriminator attribute: 'staff', 'customer'
    
    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': type
    }

    @property
    def password(self) -> str:
        return self._password
    
    @password.setter
    def password(self, new_password: str) -> None:
        """Hashes the new password and stores it.

        @param new_password The new password to set.
        """
        self._password = hashing.hash_value(new_password, salt='abcd')
    
    def __str__(self) -> str:
        return f"<Name: {self.fullname()}, Role: {self.type}>"
    
    def fullname(self) -> str:
        """! Method to get the full name of the person.

        @return The full name as a string.
        """
        return f"{self.first_name} {self.family_name}"