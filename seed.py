from database import db
from models.staff import Staff

def insert_test_data():
    # Clear existing data
    # db.drop_all()  # Warning: This deletes all data!

    # Create sample data
    Staff1 = Staff(
        _first_name='John', 
        _family_name='Doe', 
        _phone='0123456789', 
        _email="john.doe@example.com", 
        _username='john_doe', 
        _password='1234', 
        _position='Manager', 
        _department='Sales', 
        _date_joined='2021-01-01'
    )
    
    Staff2 = Staff(
        _first_name='Staff', 
        _family_name='Two', 
        _phone='0123456789', 
        _email="staff.two@example.com",
        _username='staff_two', 
        _password='1234', 
        _position='Manager', 
        _department='Sales', 
        _date_joined='2021-01-01'
    )

    Staff2 = Staff(
        _first_name='Staff', 
        _family_name='Two', 
        _phone='0123456789', 
        _email="staff.two@example.com",
        _username='staff_two', 
        _password='1234', 
        _position='Manager', 
        _department='Sales', 
        _date_joined='2021-01-01'
    )

    Staff3 = Staff(
        _first_name='Staff', 
        _family_name='Three', 
        _phone='0123456789', 
        _email="staff.three@example.com",
        _username='staff_three', 
        _password='1234', 
        _position='Manager', 
        _department='Sales', 
        _date_joined='2021-01-01'
    )
    # Staff3 = Staff(first_name='Staff', family_name='Three', phone='0123456789', email="staff.three@example.com", username='staff_three', password='1234', position='Personal Shopper', department='Sales', date_joined='2021-01-01')
    # customer1 = Customer(name='Jane Doe', email='jane@example.com')
    # customer2 = Customer(name='Alice Smith', email='alice@example.com')
    # corporate_customer1 = CorporateCustomer(name='Tech Solutions', email='info@techsolutions.com')

    # Add to session
    db.session.add(Staff1)
    db.session.add(Staff2)
    db.session.add(Staff3)
    # db.session.add(customer1)
    # db.session.add(customer2)
    # db.session.add(corporate_customer1)

    # Commit to save data
    db.session.commit()