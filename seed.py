from database import db
from models.staff import Staff
from models.customer import Customer
from models.corporate_customer import CorporateCustomer

def insert_test_data():
    # Clear existing data
    # db.drop_all()  # Warning: This deletes all data!

    # Create sample data
    # Staff
    Staff1 = Staff(
        first_name='John', 
        family_name='Doe', 
        phone='0123456789', 
        email="john.doe@example.com", 
        username='john_doe', 
        password='1234', 
        position='Manager', 
        department='Sales', 
        date_joined='2021-01-01'
    )

    Staff2 = Staff(
        first_name='Staff', 
        family_name='Two', 
        phone='0123456789', 
        email="staff.two@example.com",
        username='staff_2', 
        password='1234', 
        position='Sales Associate', 
        department='Sales', 
        date_joined='2021-01-01'
    )

    Staff3 = Staff(
        first_name='Staff', 
        family_name='Three', 
        phone='0123456789', 
        email="staff.three@example.com",
        username='staff_3', 
        password='1234', 
        position='Sales Associate', 
        department='Sales', 
        date_joined='2021-01-01'
    )
    
    # Customers
    customer1 = Customer(
        first_name='Customer', 
        family_name='One', 
        phone='0123456789', 
        email="cust.one@example.com",
        username='cust_1', 
        password='1234', 
        address='1234 Main St'
    )
    
    customer2 = Customer(
        first_name='Customer', 
        family_name='Two', 
        phone='0123456789', 
        email="cust.two@example.com",
        username='cust_2', 
        password='1234', 
        address='1234 Main St'
    )

    customer3 = Customer(
        first_name='Customer', 
        family_name='Three', 
        phone='0123456789', 
        email="cust.three@example.com",
        username='cust_3', 
        password='1234', 
        address='1234 Main St'
    )

    customer4 = Customer(
        first_name='Customer', 
        family_name='Four', 
        phone='0123456789', 
        email="cust.four@example.com",
        username='cust_4', 
        password='1234', 
        address='1234 Main St'
    )

    customer5 = Customer(
        first_name='Customer', 
        family_name='Five', 
        phone='0123456789', 
        email="cust.five@example.com",
        username='cust_5', 
        password='1234', 
        address='1234 Main St'
    )

    # Corporate Customers
    corporate_customer1 = CorporateCustomer(
        first_name='Corporate', 
        family_name='One', 
        phone='0123456789', 
        email="company.one@example.com",
        username='company1', 
        password='1234', 
        address='1234 Main St',
        company_name='Company One'
    )

    corporate_customer2 = CorporateCustomer(
        first_name='Corporate', 
        family_name='Two', 
        phone='0123456789', 
        email="company.two@example.com",
        username='company2', 
        password='1234', 
        address='1234 Main St',
        company_name='Company Two'
    )

    corporate_customer3 = CorporateCustomer(
        first_name='Corporate', 
        family_name='Three', 
        phone='0123456789', 
        email="company.three@example.com",
        username='company3', 
        password='1234', 
        address='1234 Main St',
        company_name='Company Three'
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