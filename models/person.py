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
    _phone = db.Column(db.String(11), nullable=False)
    _email = db.Column(db.String(80), unique=True, nullable=False)    
    _username = db.Column(db.String(30), unique=True, nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    type = db.Column(db.String(50)) # Discriminator attribute: 'staff', 'customer'
    
    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': type
    }

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
    
    @username.setter
    def username(self, new_username: str) -> None:
        """Method to set new username for the person.

        @param new_username The new username to set.
        """
        self._username = new_username

    @classmethod
    def find_by_username(cls, username: str):
        """! Method to find a person by username.

        @param username The username to search for.
        @return The person with the given username.
        """
        return cls.query.filter_by(_username=username).first()
    
    @property
    def password(self) -> str:
        # """Returns the hashed password. Direct access to the password is not allowed."""
        # raise AttributeError("Password is not accessible directly.")
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
    
    def check_password(self, password) -> bool:
        """Checks the hashed password against a provided password.
        
        @param password The password to check.
        @return True if the password matches, False otherwise.
        """
        return hashing.check_value(self._password, password, salt='abcd')
    


    # def __init__(self, first_name, family_name, phone, email, username, password, user_type):
    #     self._first_name = first_name
    #     self._family_name = family_name
    #     self._phone = phone
    #     self._email = email
    #     self._username = username
    #     self._password = hashing.hash_value(password)  # Hash the password
    #     self._type = user_type
    
    # @property
    # def first_name(self) -> str:
    #     """! Method to get the person's first name.
        
    #     @return The first name as a string.
    #     """
    #     return self._first_name
    
    # @first_name.setter
    # def first_name(self, new_first_name: str) -> None:
    #     """! Method to set new first name for the person.
        
    #     @param new_first_name The new first name to set.
    #     """
    #     self._first_name = new_first_name
    
    # @property  
    # def family_name(self) -> str:
    #     """! Method to get the person's family name.
        
    #     @return The family name as a string.
    #     """
    #     return self._family_name
    
    # @family_name.setter
    # def family_name(self, new_family_name: str) -> None:
    #     """! Method to set new family name for the person.
        
    #     @param new_family_name The new family name to set.
    #     """
    #     self._family_name = new_family_name
        

    # @property
    # def created_at(self) -> datetime:
    #     """Method to get the time when the person is created.

    #     @return The time when the person is created.
    #     """
    #     return self._created_at

    #     @property
    # def type(self) -> str:
    #     """Method to get the type of the person.
        
    #     @return The type of the person as a string.
    #     """
    #     return self._type
    
    # @type.setter
    # def type(self, new_type: str) -> None:
    #     """Method to set new type for the person.
        
    #     @param new_type The new type to set.
    #     """
    #     self._type = new_type
    
