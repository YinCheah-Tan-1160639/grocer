from . import db, Payment

class DebitCard(Payment):
    """! The class representing a debit card payment."""

    __tablename__ = 'debit_card_payment'

    VALID_BANKS = ['Bank A', 'Bank B', 'Bank C']

    _id = db.Column(db.Integer, db.ForeignKey('payment.id'), primary_key=True)
    __bank_name = db.Column(db.String(50), nullable=False)
    __card_number = db.Column(db.String(4), nullable=False) #TODO only store the last 4 digits

    __mapper_args__ = {
        'polymorphic_identity': 'debit_card_payment',
    }

    @property
    def id(self) -> int:
        pass

    @property
    def bank_name(self) -> str: #TODO maybe have a list of bank to choose from? a global variable?
        pass
    
    @property
    def card_number(self) -> str: #TODO only show the last 4 numbers: XXXX-XXXX-XXXX-1234
        pass

    @staticmethod
    def is_valid_card(self, card_no: str) -> bool:
        """! To validate the debit card number.
        
        @return A boolean value indicating a valid card number.
        """
        pass
