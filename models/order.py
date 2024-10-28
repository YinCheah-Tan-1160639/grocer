from datetime import datetime
from decimal import Decimal
from sqlalchemy.sql import func
from . import db, Customer, OrderLine, Payment


class Order(db.Model):
    """! The class representing an order."""
    
    __tablename__ = 'order'
    
    STATUS = ['Awaiting Payment', 'Charge to Account','Confirmed', 'Cancelled', 'Processed', 'Ready', 'Completed']

    # Class attributes
    # The discount for corporate customer for every order.
    _corporate_discount = 0.1 # 10 percent
    # The maximum delivery distance allowed.
    _max_delivery_distance = 20 # kilometres
    
    id: int = db.Column(db.Integer, primary_key=True)
    _date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _is_delivery: bool = db.Column(db.Boolean, nullable=False, default=False)
    #TODO maybe charge to account doesn't needto be recorded but update customer balance
    # _charge_to_account: bool = db.Column(db.Boolean, nullable=False, default=False)
    _payment_id: int = db.Column(db.Integer, db.ForeignKey("payment.id"))
    _customer_id: int = db.Column(db.Integer, db.ForeignKey("customer.id"))
    _status: str = db.Column(db.String(30), nullable=False)
    
    orderlines: OrderLine = db.relationship('OrderLine', back_populates='order')
    # payment: Payment = db.relationship('Payment', back_populates='order')

    @property
    def id(self) -> int:
        """! Method to get the order id.

        @return The id of the order as an integer.
        """
        pass

    @property
    def date(self) -> datetime:
        """! Method to get the order date.

        @return The date object of the order.
        """
        pass

    @property
    def customer_id(self) -> Customer:
        """! Method to get the customer object who made the payment.

        @return The Customer object.
        """
        pass

    @property
    def order_lines(self) -> str:
        """! Method to get the list of OrderItem object of the order.

        @return The list of OrderItem objects of the order.
        """
        pass

    @property
    def is_delivery(self) -> bool:
        """! Method to get the delivery requirement of the order.

        @return A boolean value indicating whether the order is a delivery order.
        """
        pass

    @property
    def status(self) -> str:
        """! Method to get the status of the order.

        @return A boolean value indicating whether the order is checked out and confirmed.
        """
        pass

    def add_item(self, item: OrderLine):
        """! Method to add item to the order.

        @param The OrderLine object to be added.
        """
        pass

    def remove_item(self, item: OrderLine):
        """! Method to remove item from the order.

        @param The OrderLine object to be removed.
        """
        pass

    def calculate_total(self) -> Decimal:
        """! Calculate to total cost of the order.

        @return The total cost of the order.
        """
        pass
    
    def can_be_delivered(self, distance: float) -> bool:
        """! To check the distance is within the maximum delivery distance.

        @return A boolean value indicating whether delivery is possible.
        """
        pass

    def update_status(self, new_status) -> None:
        """! Update the status of the order to confirmed."""
        pass