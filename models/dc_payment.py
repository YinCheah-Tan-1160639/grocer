from . import db, Payment

class DebitCard(Payment):
    """! The class representing a debit card payment."""

    __tablename__ = 'debit_card_payment'

    VALID_BANKS = ['Bank A', 'Bank B', 'Bank C']

    id = db.Column(db.Integer, db.ForeignKey('payment.id'), primary_key=True, autoincrement=True)
    bank_name = db.Column(db.String(50), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'dc_payment',
    }