from . import db, Person, Vegetable
# from .person import Person
# from .vegetable import Vegetable
from decimal import Decimal


class Customer(Person):
    """! The class representing a private customer.
    This class inherits from the Person class."""

    __tablename__ = 'customer'

    # Class attribute
    _max_owing_limit: Decimal = Decimal('100.00')

    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True, autoincrement=True)
    address = db.Column(db.String(255), nullable=False)
    _balance = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))

    # Add relationship to orders and payments associated with the customer
    orders = db.relationship('Order', back_populates='customer')
    payments = db.relationship('Payment', back_populates='customer')
    
    __mapper_args__ = {
        'polymorphic_identity': 'customer'
    }

    @property
    def balance(self) -> Decimal:
        """! Method to get the customer's balance.

        @return The customer's balance in Decimal.
        """
        return self._balance
    
    @classmethod
    def list_available_veggies(cls) -> list:
        """! Class method to list all available vegetables.
        
        @return A list of all available vegetables.
        """
        try:
            return Vegetable.get_available_vegetables()
        except Exception as e:
            raise ValueError(f"Error retrieving available vegetables: {str(e)}")
    
    def __str__(self) -> str:
        """! The string representation of the Customer object.
        
        @return The Customer object as a string.
        """
        return f"<Name: {self.fullname()}, Role: Private Customer>"
    
    def can_place_order(self) -> bool:
        """! Method to check if a customer can place order. 
        Balance not exceed max_owing_limit for customer.
        
        @return A boolean value indicating whether the customer can place order.
        """
        return self.balance < self._max_owing_limit
    
    def make_payment(self, amount: Decimal) -> None:
        """! Method to make payment for the customer.
        
        @param amount The amount to pay.
        """
        self.balance -= amount

    def update_balance(self, amount: Decimal) -> None:
        """! Method to add the total cost of an order to the customer's balance.
        
        @param amount The total cost of the order.
        """
        #TODO: Add check if the customer can place order
        self._balance += amount
    
    def details(self) -> str:
        """! Method to get customer details.
        
        @return The details of customer as a string.
        """
        return f"{self.fullname()} (ID: {self.id})\nPhone: {self.phone}Address: {self.address}\nBalance: ${self.balance}"
    
    
    # @property
    # def address(self) -> str:
    #     """! Method to get the customer's address.

    #     @return The customer's address as a string.
    #     """
    #     return self._address

    # @address.setter
    # def address(self, new_address: str) -> None:
    #     """! Method to set new address for the customer.

    #     @param new_address The new address to set.
    #     """
    #     self._address = new_address
