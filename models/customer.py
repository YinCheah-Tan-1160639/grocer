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
    
    def remaining_balance(self) -> Decimal:
        """! Method to get the remaining balance of the customer.
        
        @return The remaining balance of the customer.
        """
        return self.MAX_OWING - self.balance
    
    def can_place_order(self, amount: Decimal) -> bool:
        """! Method to check if a private customer can place order. 
        Balance can not exceed MAX_OWING limit for private customer.

        @return A boolean value indicating whether the customer can place order.
        """
        return amount <= self.remaining_balance()

    def update_balance(self, amount: Decimal) -> None:
        """! Method to add the total cost of an order to the customer's balance.
        
        @param amount The total cost of the order.
        """
        self.balance += amount

    def pay_balance(self, amount: Decimal) -> None:
        """! Method to pay the balance of the customer."""
        if amount > self.balance:
            raise ValueError("Amount exceeds the balance")
        self.balance -= amount

    def refund(self, amount: Decimal) -> None:
        """! Method to refund the customer."""
        self.balance -= amount
    
    def details(self) -> str:
        """! Method to get customer details.
        
        @return The details of customer as a string.
        """
        return f"{self.fullname()} (ID: {self.id})\nPhone: {self.phone}Address: {self.address}\nBalance: ${self.balance}"