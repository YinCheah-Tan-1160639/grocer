from . import db
from sqlalchemy.sql import func

class Payment(db.Model):
    """! The class representing a payment.
    This class is the parent class for all types of payments.
    """

    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    amount = db.Column(db.Numeric(10, 2), nullable=False)    
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    type = db.Column(db.String(50))  # 'credit_card', 'debit_card'
    
    # Declare relationship with customer and order
    customer = db.relationship('Customer', back_populates='payments')
    order = db.relationship('Order', back_populates='payment')
    
    # Declare polymorphic identity
    __mapper_args__ = {
        'polymorphic_identity': 'payment',
        'polymorphic_on': type
    }

    def __str__(self) -> str:
        """! The string representation of the Payment object."""
        return f"<Payment ID: {self.id}, Amount: {self.amount}, Date: {self.date}>"