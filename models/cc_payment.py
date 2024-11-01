from . import db, Payment

class CreditCard(Payment):
    """! The class representing a credit card payment. 
    This class inherits from the Payment class.
    """

    __tablename__ = 'credit_card_payment'

    VALID_CARD_TYPES = ['Visa', 'MasterCard']

    id = db.Column(db.Integer, db.ForeignKey('payment.id'), primary_key=True, autoincrement=True)
    card_type = db.Column(db.String(50), nullable=False) # 'Visa', 'MasterCard'
    card_number = db.Column(db.String(16), nullable=False)
    card_expiry = db.Column(db.String(5), nullable=False) # Store as MM/YY

    __mapper_args__ = {
        'polymorphic_identity': 'cc_payment',
    }