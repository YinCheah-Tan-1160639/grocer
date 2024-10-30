from . import db
from decimal import Decimal
from datetime import datetime
from sqlalchemy.sql import func

class Payment(db.Model):
    """! The class representing a payment."""

    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _amount = db.Column(db.Numeric(10, 2), nullable=False)    
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    type = db.Column(db.String(50))  # 'credit_card', 'debit_card'
    # Declare relationship with customer and order
    customer = db.relationship('Customer', back_populates='payments')
    order = db.relationship('Order', back_populates='payment')
    
    __mapper_args__ = {
        'polymorphic_identity': 'payment',
        'polymorphic_on': type
    }
    
    @property
    def amount(self) -> Decimal:
        """! Method to get the amount paid by customer.

        @return The payment amount in Decimal.
        """
        return self._amount

    def __str__(self) -> str:
        """! The string representation of the Payment object."""
        return f"<Payment ID: {self.id}, Amount: {self._amount}, Date: {self.date}>"


    #TODO how to do charge_to_account
    # charge_to_account: bool = db.Column(db.Boolean, nullable=False, default=False)

    
    # @property
    # def date(self) -> datetime:
    #     """! Method to get the payment date.

    #     @return The date object of the payment.
    #     """
    #     return self._date

    
    # @property
    # def customer_id(self) -> int:
    #     """! Method to get the customer id of customer who made the payment.

    #     @return The customer id of customer who made the payment.
    #     """
    #     return self._customer_id
    
    # @property
    # def order_id(self) -> int:
    #     """! Method to get the order id associated with the payment.

    #     @return The order id associated with the payment.
    #     """
    #     return self._order_id
    
    # @property
    # def type(self) -> str:
    #     """! Method to get the payment type.

    #     @return The payment type as a string.
    #     """
    #     return self._type
    