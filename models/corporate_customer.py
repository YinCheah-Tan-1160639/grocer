from . import db, Customer
from decimal import Decimal

class CorporateCustomer(Customer):
    """! The class representing a corporate customer.
    This class inherits from the Customer class."""

    __tablename__ = 'corporate_customer'

    # Class attribute
    # discount_rate: Decimal = Decimal('0.1') # 10 percent --> was placed in order model in part 1

    id: int = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    _company_name: str = db.Column(db.String(100), nullable=False)
    _credit_limit: Decimal = db.Column(db.Numeric(10, 2), default=Decimal('1000.00'), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'corporate_customer',
    }

    # @property
    # def id(self) -> int:
    #     pass

    @property
    def company_name(self) -> str:
        """! Method to get the corporate customer's company name.

        @return The company name as a string.
        """
        return self._company_name
    
    @company_name.setter
    def company_name(self, new_name: str) -> None:
        """! Method to set new company name for the corporate customer.

        @param new_name The new company name to set.
        """
        self._company_name = new_name

    @property
    def credit_limit(self) -> Decimal:
        """! Method to get the corporate customer's credit limit.

        @return The credit limit in Decimal.
        """
        return self._credit_limit

    @credit_limit.setter
    def credit_limit(self, new_limit: Decimal) -> None:
        """! Method to set new credit limit for the corporate customer.

        @param new_limit The new limit to set in Decimal type.
        """
        self._credit_limit = new_limit

    def credit_limit_balance(self) -> Decimal:
        """! Return the balance of the credit limit of the corporate customer.
        
        @return The balance of credit limit as a Decimal.
        """
        return self._credit_limit - self._balance

    def can_place_order(self) -> bool:
        """! Method to check if a corporate customer can place an order.
        
        @return A boolean value indicating whether the corporate customer can place an order.
        """
        #TODO Check if the owing balance is within the credit limit
        return self.balance < self.credit_limit
    
    def update_balance(self, amount: Decimal) -> None:
        """! Method to add total cost of an order to the corporate customer's balance.
        
        @param amount The total cost of order.
        """
        #TODO check if the balance is within the credit limit
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
