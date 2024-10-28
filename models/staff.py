from . import db, Person
from datetime import date

class Staff(Person):
    """! The class representing an staff.
    This class inherits from the Person class.
    """

    __tablename__ = 'staff'

    _id: int = db.Column(db.Integer, db.ForeignKey('person._id'), primary_key=True, autoincrement=True)
    _position: str = db.Column(db.String(255), nullable=False)
    _department: str = db.Column(db.String(255), nullable=False)
    _date_joined = db.Column(db.Date, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }

    @property
    def id(self) -> int:
        """! Method to get the staff id.

        @return The id of the staff as an integer.
        """
        return self._id

    @property
    def position(self) -> str:
        """! Method to get the staff's position.

        @return The position of the staff as a string.
        """
        return self._position

    @position.setter
    def position(self, new_position: str) -> None:
        """! Method to set new position for the staff.

        @param new_position The new position to set.
        """
        self._position = new_position

    @property
    def department(self) -> str:
        """! Method to get the department.

        @return The department of the staff as a string.
        """
        return self._department

    @department.setter
    def department(self, new_department: str) -> None:
        """! Method to set new department for the staff.

        @param new_department The new department to set.
        """
        self._department = new_department

    @property
    def date_joined(self) -> date:
        """! Method to get the date joined.

        @return The date joined of the staff as a string.
        """
        return self._date_joined
    
    @date_joined.setter
    def date_joined(self, new_date_joined: date) -> None:
        """! Method to set new date joined for the staff.

        @param new_date_joined The new date joined to set.
        """
        self._date_joined = new_date_joined

    def __str__(self) -> str:
        """! The string representation of the staff object.
        
        @return The staff object as a string.
        """
        return f"<Name: {self.fullname()}, role: staff>"

    # # list of customers
    # @staticmethod
    # def get_all_customers():
    #     """Static method to retrieve all customers."""
    #     return db.session.query(Customer).all()
    
    # # list of orders
    # @staticmethod
    # def get_all_orders():
    #     """Static method to retrieve all orders."""
    #     return db.session.query(Order).all()
    
    # # list of premade boxes
    # @staticmethod
    # def get_all_premade_boxes():
    #     """Static method to retrieve all premade boxes."""
    #     return db.session.query(PremadeBox).all()
    
    # # list of veggies
    # @staticmethod
    # def get_all_vegetables():
    #     """Static method to retrieve all vegetables."""
    #     return db.session.query(Vegetable).all()