from . import db, Payment
# from .payment import Payment
from datetime import datetime

class CreditCard(Payment):
    """! The class representing a credit card payment. 
    This class inherits from the Payment class.
    """

    __tablename__ = 'credit_card_payment'

    VALID_CARD_TYPES = ['Visa', 'MasterCard']

    id = db.Column(db.Integer, db.ForeignKey('payment.id'), primary_key=True, autoincrement=True)
    card_type = db.Column(db.String(50), nullable=False)
    _card_number = db.Column(db.String(4), nullable=False) # Only store the last 4 digits?
    card_expiry = db.Column(db.String(5), nullable=False) # Store as MM/YY
    #TODO find out easy way to store expiry or maybe don't store them?

    __mapper_args__ = {
        'polymorphic_identity': 'cc_payment',
    }

    @property
    def card_number(self) -> str: # only show the last 4 numbers: XXXX-XXXX-XXXX-1234
        return f"XXXX-XXXX-XXXX-{self._card_number[-4:]}"

    def is_valid_card(self, card_number: str) -> bool:
        """! To validate the credit card number.
        
        @param card_number The credit card number to validate.
        @return A boolean value indicating a valid card number.
        """
        return len(card_number) == 16 and card_number.isdigit()
    
    def is_valid_expiry(self) -> bool:
        """! To validate the expiry date of credit card.
        
        @return A boolean value indicating the card is not expired.
        """

        # Parse the expiry date
        expiry_month, expiry_year = map(int, self._card_expiry.split('/'))
        expiry_date = datetime(year=2000 + expiry_year, month=expiry_month, day=1)  # Use 1st of the month for comparison
        return expiry_date > datetime.now()  # Check if the expiry date is in the future
    
    
    # @property
    # def card_type(self) -> str: #TODO maybe have a list of card type to choose from? a global variable?
    #     return self._card_type
    