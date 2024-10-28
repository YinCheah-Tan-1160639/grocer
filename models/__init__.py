# Import individual models
# from .order import Order
# from .payment import Payment
# from .item import Item

# __all__ = ['Order', 'Payment', 'Item']

from app import db  # Import db from app.py
from .person import Person
from .staff import Staff
# from .customer import Customer
# from .corporate_customer import CorporateCustomer

__all__ = ['db', 'Person', 'Staff', 'Customer', 'CorporateCustomer']