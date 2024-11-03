from decimal import Decimal
from sqlalchemy.sql import func
from . import db, CorporateCustomer

class Order(db.Model):
    """! The class representing an order."""
    
    __tablename__ = 'order'
    
    # Class attributes
    STATUS = ['Pending', 'Confirmed', 'Cancelled', 'Ready for Pickup', 'Shipped', 'Completed'] # Status of the order that can be selected from
    CORP_DISC = Decimal('0.10') # 10 percent discount for corporate customers    
    DELIVERY_FEE = 10 # Delivery fee
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_delivery = db.Column(db.Boolean, nullable=False, default=False)
    is_charge_to_account = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String(30), nullable=False, default='Pending')
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    
    # Define relationships
    customer = db.relationship('Customer', back_populates='orders')
    orderlines = db.relationship('OrderLine', back_populates='order')
    payment = db.relationship('Payment', back_populates='order')

    def is_fulfilled(self) -> bool:
        """! Check if the order is fulfilled."""        
        return self.status in ['Ready for Pickup', 'Shipped', 'Completed']
    
    def confirm_order(self) -> None:
        """! Update the status of the order to confirmed."""
        if self.status == 'Confirmed':
            raise ValueError("Order is already confirmed")
        if self.status == 'Cancelled' or self.is_fulfilled():
            raise ValueError("Order status cannot be updated")
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
    
    def calculate_final_total(self) -> Decimal:
        """! Calculate to final cost of the order  including delivery fee if required.

        @return The final cost of the order.
        """
        if isinstance (self.customer, CorporateCustomer):
            if self.is_delivery:
                return self.calculate_corporate_total() + Order.DELIVERY_FEE
            return self.calculate_corporate_total()
        else:
            if self.is_delivery:
                return self.calculate_total() + Order.DELIVERY_FEE
            return self.calculate_total()
        
    def calculate_discount(self) -> Decimal:
        """! Calculate to discount of the order.

        @return The discount of the order.
        """
        return self.calculate_total() * Order.CORP_DISC
    
    def calculate_corporate_total(self) -> Decimal:
        """! Calculate to total cost of the order for corporate customer.

        @return The total cost of the order with discount.
        """
        return self.calculate_total() - self.calculate_discount()
    
    def corporate_total_display(self):
        """! Display the total cost of the order for corporate customer."""
        if self.is_delivery:
            return self.calculate_corporate_total(), self.calculate_discount(), Order.DELIVERY_FEE
        return self.calculate_corporate_total(), self.calculate_discount(), 0
    
    def private_total_display(self):
        """! Display the total cost of the order for private customer."""
        if self.is_delivery:
            return self.calculate_total(), 0, Order.DELIVERY_FEE
        return self.calculate_total(), 0, 0

    def charge_to_account(self) -> None:
        """! Update order to charge to account."""
        if self.customer.can_place_order(self.calculate_final_total()):
            self.customer.update_balance(self.calculate_final_total())
            self.is_charge_to_account = True
            self.confirm_order()
        else:
            if isinstance (self.customer, CorporateCustomer):
                raise ValueError("Order exceeds credit limit.")
            raise ValueError("Order exceeds maximum owing limit.")

    def has_payment(self) -> bool:
        """! Check if the order has payment."""
        return len(self.payment) > 0

    def cancel_order(self) -> None:
        """! Update the status of the order to cancelled."""
        if self.status == 'Cancelled':
            raise ValueError("Order is already cancelled")
        if self.is_fulfilled():
            raise ValueError("Order cannot be cancelled")
        
        # Refund the customer if there is payment/ charge to account
        if self.has_payment():
            print(self.payment)
            self.customer.refund(self.calculate_final_total())
        elif self.is_charge_to_account:
            self.customer.refund(self.calculate_final_total())
            self.is_charge_to_account = False

        self.status = 'Cancelled'
    
    def can_be_processed(self) -> bool:
        """! Check if the order can be processed."""
        return self.status == 'Confirmed'

    def update_status(self, new_status) -> None:
        """! Update the status of the order to pick up or delivery.

        @param new_status The new status of the order.
        """            
        if self.status == 'Completed':
            raise ValueError("Completed order cannot be updated")
        if new_status not in ['Ready for Pickup', 'Shipped', 'Completed']:
            raise ValueError("Invalid status")
        if new_status in self.status:
            raise ValueError("Order is already in this status")       
        # if not self.can_be_processed():
        #     raise ValueError("Order has not been confirmed")
        if self.is_delivery and new_status == 'Ready for Pickup':
            raise ValueError("This is a delivery order")
        if new_status == 'Shipped' and not self.is_delivery:
            raise ValueError("This is not a delivery order")
        self.status = new_status