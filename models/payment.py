from . import db
from decimal import Decimal
from datetime import datetime
from sqlalchemy.sql import func

class Payment(db.Model):
    """! The class representing a payment."""

    __tablename__ = 'payment'

    _id = db.Column(db.Integer, primary_key=True)
    _amount = db.Column(db.Decimal(10, 2), nullable=False)
    _date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    #TODO Maybe charge_to_account attribute is for order class
    # charge_to_account: bool = db.Column(db.Boolean, nullable=False, default=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    #TODO find out how to do the relationship here
    # order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    # or
    # order: Order = db.relationship('Order', back_populates='payment')
    _type = db.Column(db.String(50))  # 'credit_card', 'debit_card'

    __mapper_args__ = {
        'polymorphic_identity': 'payment',
        'polymorphic_on': _type
    }

    @property
    def id(self) -> int:
        """! Method to get the payment id.

        @return The id of the payment as an integer.
        """
        pass

    @property
    def date(self) -> datetime:
        """! Method to get the payment date.

        @return The date object of the payment.
        """
        pass
    
    @property
    def amount(self) -> Decimal:
        """! Method to get the amount paid by customer.

        @return The payment amount in Decimal.
        """
        pass

    @property
    def customer_id(self) -> Customer:
        """! Method to get the customer object who made the payment.

        @return The Customer object.
        """
        pass