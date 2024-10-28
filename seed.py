from database import db
from models.staff import Staff
from models.customer import Customer
from models.corporate_customer import CorporateCustomer

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
        _username='staff_2', 
        _password='1234', 
        _position='Sales Associate', 
        _department='Sales', 
        _date_joined='2021-01-01'
    )

    Staff3 = Staff(
        _first_name='Staff', 
        _family_name='Three', 
        _phone='0123456789', 
        _email="staff.three@example.com",
        _username='staff_3', 
        _password='1234', 
        _position='Sales Associate', 
        _department='Sales', 
        _date_joined='2021-01-01'
    )
    
    customer1 = Customer(
        _first_name='Customer', 
        _family_name='One', 
        _phone='0123456789', 
        _email="cust.one@example.com",
        _username='cust_1', 
        _password='1234', 
        _address='1234 Main St'
    )
    
    customer2 = Customer(
        _first_name='Customer', 
        _family_name='Two', 
        _phone='0123456789', 
        _email="cust.two@example.com",
        _username='cust_2', 
        _password='1234', 
        _address='1234 Main St'
    )

    customer3 = Customer(
        _first_name='Customer', 
        _family_name='Three', 
        _phone='0123456789', 
        _email="cust.three@example.com",
        _username='cust_3', 
        _password='1234', 
        _address='1234 Main St'
    )

    customer4 = Customer(
        _first_name='Customer', 
        _family_name='Four', 
        _phone='0123456789', 
        _email="cust.four@example.com",
        _username='cust_4', 
        _password='1234', 
        _address='1234 Main St'
    )

    customer5 = Customer(
        _first_name='Customer', 
        _family_name='Five', 
        _phone='0123456789', 
        _email="cust.five@example.com",
        _username='cust_5', 
        _password='1234', 
        _address='1234 Main St'
    )

    corporate_customer1 = CorporateCustomer(
        _first_name='Corporate', 
        _family_name='One', 
        _phone='0123456789', 
        _email="company.one@example.com",
        _username='company1', 
        _password='1234', 
        _address='1234 Main St',
        _company_name='Company One'
    )

    corporate_customer2 = CorporateCustomer(
        _first_name='Corporate', 
        _family_name='Two', 
        _phone='0123456789', 
        _email="company.two@example.com",
        _username='company2', 
        _password='1234', 
        _address='1234 Main St',
        _company_name='Company Two'
    )

    corporate_customer3 = CorporateCustomer(
        _first_name='Corporate', 
        _family_name='Three', 
        _phone='0123456789', 
        _email="company.three@example.com",
        _username='company3', 
        _password='1234', 
        _address='1234 Main St',
        _company_name='Company Three'
    )

    # Add to session
    db.session.add(Staff1)
    db.session.add(Staff2)
    db.session.add(Staff3)
    db.session.add(customer1)
    db.session.add(customer2)
    db.session.add(customer3)
    db.session.add(customer4)
    db.session.add(customer5)
    db.session.add(corporate_customer1)
    db.session.add(corporate_customer2)
    db.session.add(corporate_customer3)

    # Commit to save data
    db.session.commit()