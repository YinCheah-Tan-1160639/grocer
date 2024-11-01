from . import db, Customer
from decimal import Decimal

class CorporateCustomer(Customer):
    """! The class representing a corporate customer.
    This class inherits from the Customer class."""

    __tablename__ = 'corporate_customer'

    id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(100), nullable=False)
    credit_limit = db.Column(db.Numeric(10, 2), default=Decimal('1000.00'), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'corporate_customer',
    }
    
    def can_place_order(self) -> bool:
        """! Method to check if a corporate customer can place an order.
        
        @return A boolean value indicating whether the corporate customer can place an order.
        """
        return self.balance < self.credit_limit
    
    def update_balance(self, amount: Decimal) -> None:
        """! Method to add total cost of an order to the corporate customer's balance.
        
        @param amount The total cost of order.
        """
        if self.can_place_order():
            self.balance += amount

    def details(self) -> str:
        """! Method to get corporate customer details.
        
        @return The details of the corporate customer as a string.
        """
        return f"{self.fullname()} (ID: {self.id})\nPhone: {self.phone}Company: {self.company_name}\nBalance: ${self.balance}\nCredit Limit: {self.credit_limit}"
    
    def __str__(self) -> str:
        """! The string representation of the Customer object.
        
        @return The Customer object as a string.
        """
        return f"<Name: {self.fullname()}, Role: Corporate Customer>"



    # Class attribute
    # discount_rate: Decimal = Decimal('0.1') # 10 percent --> was placed in order model in part 1

    
    # @property
    # def company_name(self) -> str:
    #     """! Method to get the corporate customer's company name.

    #     @return The company name as a string.
    #     """
    #     return self._company_name
    
    # @company_name.setter
    # def company_name(self, new_name: str) -> None:
    #     """! Method to set new company name for the corporate customer.

    #     @param new_name The new company name to set.
    #     """
    #     self._company_name = new_name
