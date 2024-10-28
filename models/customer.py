from . import db, Person
from decimal import Decimal


class Customer(Person):
    """! The class representing a private customer.
    This class inherits from the Person class."""

    __tablename__ = 'customer'

    # Class attribute
    _max_owing_limit: Decimal = Decimal('100.00')

    id: int = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True, autoincrement=True)
    _address: str = db.Column(db.String(255), nullable=False)
    _balance: Decimal = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    
    __mapper_args__ = {
        'polymorphic_identity': 'customer'
    }

    # Add relationship to orders and payments associated with the person
    # orders: Order = db.relationship('Order', back_populates='customer')
    # payments: Payment = db.relationship('Payment', back_populates='customer')

    # @property
    # def id(self) -> int:
    #     """! Method to get the customer's id.

    #     @return The id as an integer.
    #     """
    #     return self._id

    @property
    def address(self) -> str:
        """! Method to get the customer's address.

        @return The customer's address as a string.
        """
        return self._address

    @address.setter
    def address(self, new_address: str) -> None:
        """! Method to set new address for the customer.

        @param new_address The new address to set.
        """
        self._address = new_address

    @property
    def balance(self) -> Decimal:
        """! Method to get the customer's balance.

        @return The customer's balance in Decimal.
        """
        return self._balance
    
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
        self.balance += amount
    
    def details(self) -> str:
        """! Method to get customer details.
        
        @return The details of customer as a string.
        """
        return f"{self.fullname()} (ID: {self.id})\nPhone: {self.phone}Address: {self.address}\nBalance: ${self.balance}"