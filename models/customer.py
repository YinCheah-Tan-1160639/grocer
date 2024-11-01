from . import db, Person
from decimal import Decimal

class Customer(Person):
    """! The class representing a private customer.
    This class inherits from the Person class."""

    __tablename__ = 'customer'

    # Class attribute
    MAX_OWING: Decimal = Decimal('100.00')

    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True, autoincrement=True)
    address = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))

    # Add relationship to orders and payments associated with the customer
    orders = db.relationship('Order', back_populates='customer')
    payments = db.relationship('Payment', back_populates='customer')
    
    __mapper_args__ = {
        'polymorphic_identity': 'customer'
    }

    def __str__(self) -> str:
        """! The string representation of the Customer object.
        
        @return The Customer object as a string.
        """
        return f"<Name: {self.fullname()}, Role: Private Customer>"
    
    def can_place_order(self) -> bool:
        """! Method to check if a private customer can place order. 
        Balance can not exceed MAX_OWING limit for private customer.

        @return A boolean value indicating whether the customer can place order.
        """
        return self.balance < self.MAX_OWING
    
    def make_payment(self, amount: Decimal) -> None:
        """! Method to make payment for the customer.
        
        @param amount The amount paid.
        """
        self.balance -= amount

    def update_balance(self, amount: Decimal) -> None:
        """! Method to add the total cost of an order to the customer's balance.
        
        @param amount The total cost of the order.
        """
        if self.can_place_order():
            self.balance += amount
    
    def details(self) -> str:
        """! Method to get customer details.
        
        @return The details of customer as a string.
        """
        return f"{self.fullname()} (ID: {self.id})\nPhone: {self.phone}Address: {self.address}\nBalance: ${self.balance}"