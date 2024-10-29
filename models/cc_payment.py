from . import db, Payment

class CreditCard(Payment):
    """! The class representing a credit card payment. This class inherits from the Payment class."""

    __tablename__ = 'credit_card_payment'

    VALID_CARD_TYPES = ['Visa', 'MasterCard', 'Amex']

    _id = db.Column(db.Integer, db.ForeignKey('payment.id'), primary_key=True)
    __card_type = db.Column(db.String(50), nullable=False)
    __card_number = db.Column(db.String(4), nullable=False) #TODO only store the last 4 digits
    __card_expiry = db.Column(db.String(5), nullable=False) #TODO find out easy way to store expiry or maybe don't store them?

    __mapper_args__ = {
        'polymorphic_identity': 'credit_card_payment',
    }

    @property
    def id(self) -> int:
        pass

    @property
    def card_type(self) -> str: #TODO maybe have a list of card type to choose from? a global variable?
        pass
    
    @property
    def card_number(self) -> str: # only show the last 4 numbers: XXXX-XXXX-XXXX-1234
        return f"XXXX-XXXX-XXXX-{self.__card_number[-4:]}"

    @staticmethod
    def is_valid_card(self, card_no: str) -> bool:
        """! To validate the credit card number.
        
        @return A boolean value indicating a valid card number.
        """
        pass
    
    @staticmethod
    def is_valid_expiry(self, expiry: str) -> bool:
        """! To validate the expiry date of credit card.
        
        @return A boolean value indicating the card is not expired.
        """
        pass