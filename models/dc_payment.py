from . import db, Payment
# from .payment import Payment

class DebitCard(Payment):
    """! The class representing a debit card payment."""

    __tablename__ = 'debit_card_payment'

    VALID_BANKS = ['Bank A', 'Bank B', 'Bank C']

    id = db.Column(db.Integer, db.ForeignKey('payment.id'), primary_key=True, autoincrement=True)
    bank_name = db.Column(db.String(50), nullable=False)
    _card_number = db.Column(db.String(4), nullable=False) #TODO only store the last 4 digits

    __mapper_args__ = {
        'polymorphic_identity': 'dc_payment',
    }

    @property
    def card_number(self) -> str: #TODO only show the last 4 numbers: XXXX-XXXX-XXXX-1234
        return f"XXXX-XXXX-XXXX-{self._card_number[-4:]}"

    def is_valid_card(self, card_number: str) -> bool:
        """! To validate the credit card number.
        
        @param card_number The credit card number to validate.
        @return A boolean value indicating a valid card number.
        """
        return len(card_number) == 16 and card_number.isdigit()
    
    
    # @property
    # def bank_name(self) -> str: #TODO maybe have a list of bank to choose from? a global variable?
    #     return self._bank_name
    
