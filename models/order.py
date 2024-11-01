from decimal import Decimal
from sqlalchemy.sql import func
from . import db

class Order(db.Model):
    """! The class representing an order."""
    
    __tablename__ = 'order'
    
    # Class attributes
    STATUS = ['Pending', 'Confirmed', 'Cancelled', 'Ready for Pickup', 'Shipped', 'Completed'] # Status of the order that can be selected from
    CORP_DISC = Decimal('0.10') # 10 percent discount for corporate customers    
    DELIVERY_FEE = Decimal(10)
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    is_delivery = db.Column(db.Boolean, nullable=False, default=False)
    # is_confirmed = db.Column(db.Boolean, nullable=False, default=False) # checked out --> update status to confirmed
    is_charge_to_account = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String(30), nullable=False, default='Pending')
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    
    # Define relationships
    customer = db.relationship('Customer', back_populates='orders')
    orderlines = db.relationship('OrderLine', back_populates='order')
    payment = db.relationship('Payment', back_populates='order')
    
    def confirm_order(self) -> None:
        """! Update the status of the order to confirmed."""
        if self.status == 'Confirmed':
            raise ValueError("Order is already confirmed")
        if self.status in ['Cancelled', 'Ready for Pickup', 'Shipped', 'Completed']:
            raise ValueError("Order status cannot be updated")
        if self.status == 'Pending':
            self.status = 'Confirmed'
    
    def require_delivery(self) -> bool:
        """! To update delivery requirement.

        @return A boolean value indicating whether is a delivery order.
        """
        self.is_delivery = True

    def calculate_total(self) -> Decimal:
        """! Calculate to total cost of the order.

        @return The total cost of the order.
        """
        return sum(orderline.item.calculate_subtotal() for orderline in self.orderlines) 
    
    def calculate_total_with_delivery(self) -> Decimal:
        """! Calculate to total cost of the order with delivery fee.

        @return The total cost of the order with delivery fee.
        """
        return self.calculate_total() + Order.DELIVERY_FEE
    
    def calculate_corporate_total(self) -> Decimal:
        """! Calculate to total cost of the order for corporate customer.

        @return The total cost of the order with discount.
        """
        discount = self.calculate_total() * Order.CORP_DISC
        total = self.calculate_total() - discount
        if self.is_delivery:
            total += Order.DELIVERY_FEE
            return discount, total
        else:
            return discount, total

    def charge_to_account(self) -> None:
        """! Update order to charge to account."""
        if not self.is_charge_to_account:
            self.is_account_charge = True
            # self.customer.balance += self.calculate_total() --> call in controller
        else:
            raise ValueError("Order is already charged to account")

    def cancel_order(self) -> None:
        """! Update the status of the order to cancelled."""
        if not self.status not in ['Cancelled', 'Ready for Pickup', 'Shipped', 'Completed']:
            self.update_status('Cancelled')
        else:
            if self.status == 'Cancelled':
                raise ValueError("Order is already cancelled")
            elif self.status in ['Ready for Pickup', 'Shipped', 'Completed']:
                raise ValueError("Order cannot be cancelled")
            
    def has_payment(self) -> bool:
        """! Check if the order has payment."""
        return self.payment is not None
    
    def can_be_processed(self) -> bool:
        """! Check if the order can be processed."""
        return (self.has_payment() or self.is_charge_to_account) and self.status == 'Confirmed'

    def update_status(self, new_status) -> None:
        """! Update the status of the order to pick up or delivery.

        @param new_status The new status of the order.
        """            
        if new_status not in ['Ready for Pickup', 'Shipped', 'Completed']:
            raise ValueError("Invalid status")
        if new_status in self.status:
            raise ValueError("Order is already in this status")       
        if not self.can_be_processed():
            raise ValueError("Order has not been paid")
        if self.status == 'Completed' and new_status in ['Ready for Pickup', 'Shipped']:
            raise ValueError("Completed order cannot be updated")
        if self.is_delivery and new_status == 'Ready for Pickup':
            raise ValueError("This is a delivery order")
        if new_status == 'Shipped' and not self.is_delivery:
            raise ValueError("This is not a delivery order")
        self.status = new_status