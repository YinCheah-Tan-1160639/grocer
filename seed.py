from database import db
from models.staff import Staff
from models.customer import Customer
from models.corporate_customer import CorporateCustomer
# from models.product import Product
# from models.unit_price_veggie import UnitPriceVeggie
# from models.weighted_veggie import WeightedVeggie
# from models.pack_veggie import PackVeggie

def insert_test_data():
    # Clear existing data
    # db.drop_all()  # Warning: This deletes all data!

    # Create sample data

    # Create empty staff list
    staffs = []
    customers = []
    corporate_customers = []

    # Add staff instances to the list
    staffs.append(Staff(
        first_name='John', 
        family_name='Doe', 
        phone='0123456789', 
        email="john.doe@example.com", 
        username='john_doe', 
        password='1234', 
        position='Manager', 
        department='Sales', 
        date_joined='2021-01-01'
    ))

    staffs.append(Staff(
        first_name='Staff', 
        family_name='Two', 
        phone='0123456789', 
        email="staff.two@example.com",
        username='staff_2', 
        password='1234', 
        position='Sales Associate', 
        department='Sales', 
        date_joined='2021-01-01'
    ))

    staffs.append(Staff(
        first_name='Staff', 
        family_name='Three', 
        phone='0123456789', 
        email="staff.three@example.com",
        username='staff_3', 
        password='1234', 
        position='Sales Associate', 
        department='Sales', 
        date_joined='2021-01-01'
    ))
    
    # Customers
    customers.append(Customer(
        first_name='Customer', 
        family_name='One', 
        phone='0123456789', 
        email="cust.one@example.com",
        username='cust_1', 
        password='1234', 
        address='1234 Main St'
    ))
    
    customers.append(Customer(
        first_name='Customer', 
        family_name='Two', 
        phone='0123456789', 
        email="cust.two@example.com",
        username='cust_2', 
        password='1234', 
        address='1234 Main St'
    ))

    customers.append(Customer(
        first_name='Customer', 
        family_name='Three', 
        phone='0123456789', 
        email="cust.three@example.com",
        username='cust_3', 
        password='1234', 
        address='1234 Main St'
    ))

    customers.append(Customer(
        first_name='Customer', 
        family_name='Four', 
        phone='0123456789', 
        email="cust.four@example.com",
        username='cust_4', 
        password='1234', 
        address='1234 Main St'
    ))

    customers.append(Customer(
        first_name='Customer', 
        family_name='Five', 
        phone='0123456789', 
        email="cust.five@example.com",
        username='cust_5', 
        password='1234', 
        address='1234 Main St'
    ))

    # Corporate Customers
    corporate_customers.append(CorporateCustomer(
        first_name='Corporate', 
        family_name='One', 
        phone='0123456789', 
        email="company.one@example.com",
        username='company1', 
        password='1234', 
        address='1234 Main St',
        company_name='Company One'
    ))

    corporate_customers.append(CorporateCustomer(
        first_name='Corporate', 
        family_name='Two', 
        phone='0123456789', 
        email="company.two@example.com",
        username='company2', 
        password='1234', 
        address='1234 Main St',
        company_name='Company Two'
    ))

    corporate_customers.append(CorporateCustomer(
        first_name='Corporate', 
        family_name='Three', 
        phone='0123456789', 
        email="company.three@example.com",
        username='company3', 
        password='1234', 
        address='1234 Main St',
        company_name='Company Three'
    ))

    # w_veggie1 = WeightedVeggie(
    #     orderline_id=1,
    #     name='Carrots', 
    #     price_per_kg=2.89, 
    #     weight=0.5
    # )

    # w_veggie2 = WeightedVeggie(
    #     orderline_id=2,
    #     name='Tomatoes', 
    #     price_per_kg=4.99, 
    #     weight=1.2
    # )

    # w_veggie3 = WeightedVeggie(
    #     orderline_id=3,
    #     name='Gingers', 
    #     price_per_kg=9.99, 
    #     weight=0.2
    # )

    # w_veggie4 = WeightedVeggie(
    #     orderline_id=4,
    #     name='Onions', 
    #     price_per_kg=0.99, 
    #     weight=0.3
    # )

    # w_veggie5 = WeightedVeggie(
    #     orderline_id=5,
    #     name='Kumaras', 
    #     price_per_kg=5.99, 
    #     weight=2.0
    # )

    # p_veggie1 = PackVeggie(
    #     orderline_id=6,
    #     name='Carrots (1.5kg)', 
    #     price_per_pack=2.89, 
    #     no_of_pack=0.5
    # )

    # p_veggie2 = PackVeggie(
    #     orderline_id=7,
    #     name='Baby Spinach (130g)', 
    #     price_per_pack=3.99, 
    #     no_of_pack=2
    # )

    # p_veggie3 = PackVeggie(
    #     orderline_id=8,
    #     name='Washed Lettuce (250g)', 
    #     price_per_pack=5.99, 
    #     no_of_pack=1
    # )

    # p_veggie4 = PackVeggie(
    #     orderline_id=9,
    #     name='Shredded Cabbage (200g)', 
    #     price_per_pack=3.99, 
    #     no_of_pack=1
    # )

    # p_veggie5 = PackVeggie(
    #     orderline_id=10,
    #     name='Red Potatoes (5kg)', 
    #     price_per_pack=10.99, 
    #     no_of_pack=1
    # )

    # u_veggie1 = UnitPriceVeggie(
    #     orderline_id=11,
    #     name='Cabbage', 
    #     price_per_unit=2.89,
    #     quantity=1
    # )

    # u_veggie2 = UnitPriceVeggie(
    #     orderline_id=12,
    #     name='Brocolli', 
    #     price_per_unit=1.99,
    #     quantity=1
    # )

    # u_veggie3 = UnitPriceVeggie(
    #     orderline_id=13,
    #     name='Cauliflower', 
    #     price_per_unit=3.99,
    #     quantity=1
    # )

    # u_veggie4 = UnitPriceVeggie(
    #     orderline_id=14,
    #     name='Pumpkin', 
    #     price_per_unit=5.99,
    #     quantity=1
    # )

    # u_veggie5 = UnitPriceVeggie(
    #     orderline_id=15,
    #     name='Cucumber', 
    #     price_per_unit=3.99,
    #     quantity=2
    # )

    # Add to session
    db.session.add_all(staffs)
    db.session.add_all(customers)
    db.session.add_all(corporate_customers)
    # db.session.add(w_veggies)
    # db.session.add(p_veggies)
    # db.session.add(u_veggies)

    # Commit to save data
    db.session.commit()