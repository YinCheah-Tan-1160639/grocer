from . import db, Person, Vegetable

# from .person import Person
# from .vegetable import Vegetable
from datetime import date

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
    
    @classmethod
    def list_all_customers(cls) -> list:
        """! Class method to get all customers.
        
        @return A list of Customer instances .
        """
        return Person.query.filter(
            Person.type.in_(["customer", "corporate_customer"]
            )).order_by(
                Person.family_name,
                Person.first_name
            ).all()
    
    @classmethod
    def get_customer_details(cls, customer_id: int) -> Person:
        """! Class method to get customer details.
        
        @param customer_id The id of the customer.
        @return The customer details.
        """
        customer = Person.query.get_or_404(customer_id)

        if customer.type not in ["customer", "corporate_customer"]:
            raise ValueError("Invalid customer type.")
        return customer
    
    @classmethod
    def list_all_veggies(cls) -> list:
        """! Class method to get all vegetables.
        
        @return A list of Vegetable instances.
        """
        return Vegetable.get_all_vegetables()

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
    
    # @property
    # def id(self) -> int:
    #     """! Method to get the staff id.

    #     @return The id of the staff as an integer.
    #     """
    #     return self._id


    # @property
    # def position(self) -> str:
    #     """! Method to get the staff's position.

    #     @return The position of the staff as a string.
    #     """
    #     return self._position

    # @position.setter
    # def position(self, new_position: str) -> None:
    #     """! Method to set new position for the staff.

    #     @param new_position The new position to set.
    #     """
    #     self._position = new_position

    # @property
    # def department(self) -> str:
    #     """! Method to get the department.

    #     @return The department of the staff as a string.
    #     """
    #     return self._department

    # @department.setter
    # def department(self, new_department: str) -> None:
    #     """! Method to set new department for the staff.

    #     @param new_department The new department to set.
    #     """
    #     self._department = new_department

    # @property
    # def date_joined(self) -> date:
    #     """! Method to get the date joined.

    #     @return The date joined of the staff as a string.
    #     """
    #     return self._date_joined
    
    # @date_joined.setter
    # def date_joined(self, new_date_joined: date) -> None:
    #     """! Method to set new date joined for the staff.

    #     @param new_date_joined The new date joined to set.
    #     """
    #     self._date_joined = new_date_joined