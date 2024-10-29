from datetime import datetime
from decimal import Decimal
from sqlalchemy.sql import func
from . import db, Customer, OrderLine, Payment


class Order(db.Model):
    """! The class representing an order."""
    
    __tablename__ = 'order'
    
    STATUS = ['Pending', 'Cancelled', 'Processed', 'Ready', 'Delivered', 'Completed']

    # Class attributes
    # The discount for corporate customer for every order.
    _corporate_discount = 0.1 # 10 percent
    # The maximum delivery distance allowed.
    _max_delivery_distance = 20 # kilometres
    
    id = db.Column(db.Integer, primary_key=True)
    _date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _is_delivery = db.Column(db.Boolean, nullable=False, default=False)
    _submitted = db.Column(db.Boolean, nullable=False, default=False)
    _status = db.Column(db.String(30), nullable=False, default='Pending')
    _customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    
    customer = db.relationship('Customer', backpopulates='orders')
    orderlines = db.relationship('OrderLine', back_populates='order')
    payment = db.relationship('Payment', back_populates='order')

    @property
    def date(self) -> datetime:
        """! Method to get the order date.

        @return The date object of the order.
        """
        return self._date
    
    @property
    def is_delivery(self) -> bool:
        """! Method to get the delivery requirement of the order.

        @return A boolean value indicating whether the order is a delivery order.
        """
        #TODO add check here to make sure it is lass than 20km
        return self._is_delivery

    @property
    def is_submitted(self) -> bool:
        """! Method to check whether the order has been checked out.

        @return A boolean value indicating whether the order has been checked out.
        """
        return self._submitted

    @property
    def status(self) -> str:
        """! Method to get the status of the order.

        @return A string value indicating status of the order.
        """
        return self._status

    @property
    def customer_id(self) -> Customer:
        """! Method to get the customer object who made the payment.

        @return The Customer object.
        """
        pass

    def calculate_total(self) -> Decimal:
        """! Calculate to total cost of the order.

        @return The total cost of the order.
        """
        return sum(item.calculate_subtotal() for item in self.orderlines)
    
    def require_delivery(self) -> bool:
        """! To check the distance is within the maximum delivery distance.

        @return A boolean value indicating whether delivery is possible.
        """
        #TODO check if can be delivered
        self.is_delivery = True

    def update_status(self, new_status) -> None:
        """! Update the status of the order to confirmed."""
        pass

    def submit_order(self) -> None:
        """! Update the status of the order to submitted."""
        #TODO check 
        self.is_submitted = True

    #TODO maybe charge to account doesn't needto be recorded but update customer balance
    # _charge_to_account: bool = db.Column(db.Boolean, nullable=False, default=False)
    # _payment_id: int = db.Column(db.Integer, db.ForeignKey("payment.id"))
    # _total: Decimal = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))

    # @property
    # def order_lines(self) -> str:
    #     """! Method to get the list of OrderItem object of the order.

    #     @return The list of OrderItem objects of the order.
    #     """
    #     pass

    # def add_item(self, item: OrderLine):
    #     """! Method to add item to the order.

    #     @param The OrderLine object to be added.
    #     """
    #     pass

    # def remove_item(self, item: OrderLine):
    #     """! Method to remove item from the order.

    #     @param The OrderLine object to be removed.
    #     """
    #     pass