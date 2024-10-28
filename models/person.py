from . import db
from sqlalchemy.sql import func
from datetime import datetime

class Person(db.Model):
    """! The class representing a person."""
    __tablename__ = 'person'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _first_name = db.Column(db.String(50), nullable=False)
    _family_name = db.Column(db.String(50), nullable=False)
    _phone = db.Column(db.String(11), nullable=False)
    _email = db.Column(db.String(80), unique=True, nullable=False)    
    _username = db.Column(db.String(30), unique=True, nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    _created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    _type = db.Column(db.String(50)) # Discriminator attribute: 'staff', 'customer'
    
    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': _type
    }

    @property
    def id(self) -> int:
        """! Method to get the person's ID.
        
        @return The ID as an int.
        """
        return self._id
    
    @property
    def first_name(self) -> str:
        """! Method to get the person's first name.
        
        @return The first name as a string.
        """
        return self._first_name
    
    @first_name.setter
    def first_name(self, new_first_name: str) -> None:
        """! Method to set new first name for the person.
        
        @param new_first_name The new first name to set.
        """
        self._first_name = new_first_name
    
    @property  
    def family_name(self) -> str:
        """! Method to get the person's family name.
        
        @return The family name as a string.
        """
        return self._family_name
    
    @family_name.setter
    def family_name(self, new_family_name: str) -> None:
        """! Method to set new family name for the person.
        
        @param new_family_name The new family name to set.
        """
        self._family_name = new_family_name
    
    @property
    def phone(self) -> str:
        """! Method to get the person's phone number.
        
        @return The phone number as a string.
        """
        return self._phone
    
    @phone.setter
    def phone(self, new_phone: str) -> None:
        """! Method to set new phone number for the person.
        
        @param new_phone The new phone number to set.
        """
        self._phone = new_phone
    
    @property
    def email(self) -> str:
        """! Method to get the person's email address.

        @return The email address as a string.
        """
        return self._email
    
    @email.setter
    def email(self, new_email: str) -> None:
        """! Method to set new email for the person.
        
        @param new_email The new email address to set.
        """
        self._email = new_email
    
    @property
    def username(self) -> str:
        """Method to get username of the person.
        
        @return The username as a string.
        """
        return self._username
    
    # @username.setter
    # def username(self, new_username: str) -> None:
    #     """Method to set new username for the person.

    #     @param new_username The new username to set.
    #     """
    #     self._username = new_username
    
    @property
    def password(self) -> str:
        """Returns the hashed password. Direct access to the password is not allowed."""
        raise AttributeError("Password is not accessible directly.")
    
    @password.setter
    def password(self, new_password: str) -> None:
        """Hashes the new password and stores it.

        @param new_password The new password to set.
        """
        self._password = new_password

    @property
    def created_at(self) -> datetime:
        """Method to get the time when the person is created."""
        return self.__created_at
    
    @property
    def type(self) -> str:
        """Method to get the type of the person."""
        return self._type
    
    def __str__(self) -> str:
        return f"<Name: {self.fullname()}, Role: {self._type}>"
    
    def fullname(self) -> str:
        return f"{self._first_name} {self._family_name}"
    
    def check_password(self, password) -> bool:
        """Checks the hashed password against a provided password."""
        pass
    

    

