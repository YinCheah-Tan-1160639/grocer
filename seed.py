from database import db
from hashing import hashing
from datetime import datetime
from models import Staff, order
from models import Customer
from models import CorporateCustomer
from models import Order
from models import OrderLine
from models import PackVeggie
from models import WeightedVeggie
from models import UnitPriceVeggie
from models import CreditCard, DebitCard
from models import PremadeBox
from models import VegetableProduct
from models import PremadeBoxProduct
from models import BoxComponent

password = hashing.hash_value('Test123456', salt='abcd')

# Load and parse a text file to create product objects
def load_products(txt_file):
    with open(txt_file, 'r') as file:
        products = []
        for line in file:
            product = line.strip().split(', ')
            if len(product) != 4:
                print(f"Skipping invalid line: {line.strip()}")
                continue
            
            name, price_str, available, unit = product

            # Convert the price and available fields to the correct types
            try:
                price = float(price_str)  # Convert price to float
                available = available.lower() in ('true', '1')  # Convert to boolean
            except ValueError as e:
                print(f"Error converting line '{line.strip()}': {e}")
                continue

            products.append(VegetableProduct(name=name, price=price, available=available, unit=unit))
        db.session.add_all(products)
        db.session.commit()

# Insert test data into the database
def insert_test_data():

    # Create empty list
    staffs = []
    customers = []
    corporate_customers = []
    orders = []
    orderlines = []
    items = []
    payments = []

    # Add staff instances to the list
    staffs.append(Staff(
        first_name='John', 
        family_name='Doe', 
        phone='0123456789', 
        email="john.doe@example.com", 
        username='john_doe', 
        password=password, 
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
        password=password, 
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
        password=password, 
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
        password=password, 
        address='1234 Main St',
        balance=29.83
    ))
    
    customers.append(Customer(
        first_name='Customer', 
        family_name='Two', 
        phone='0123456789', 
        email="cust.two@example.com",
        username='cust_2', 
        password=password, 
        address='1234 Main St',
        balance=49.90
    ))

    customers.append(Customer(
        first_name='Customer', 
        family_name='Three', 
        phone='0123456789', 
        email="cust.three@example.com",
        username='cust_3', 
        password=password, 
        address='1234 Main St'
    ))

    customers.append(Customer(
        first_name='Customer', 
        family_name='Four', 
        phone='0123456789', 
        email="cust.four@example.com",
        username='cust_4', 
        password=password, 
        address='1234 Main St'
    ))

    customers.append(Customer(
        first_name='Customer', 
        family_name='Five', 
        phone='0123456789', 
        email="cust.five@example.com",
        username='cust_5', 
        password=password, 
        address='1234 Main St',
        balance=4.99
    ))

    # Corporate Customers
    corporate_customers.append(CorporateCustomer(
        first_name='Corporate', 
        family_name='One', 
        phone='0123456789', 
        email="company.one@example.com",
        username='company1', 
        password=password, 
        address='1234 Main St',
        company_name='Company One'
    ))

    corporate_customers.append(CorporateCustomer(
        first_name='Corporate', 
        family_name='Two', 
        phone='0123456789', 
        email="company.two@example.com",
        username='company2', 
        password=password, 
        address='1234 Main St',
        company_name='Company Two'
    ))

    corporate_customers.append(CorporateCustomer(
        first_name='Corporate', 
        family_name='Three', 
        phone='0123456789', 
        email="company.three@example.com",
        username='company3', 
        password=password, 
        address='1234 Main St',
        company_name='Company Three'
    ))

    # Add to session
    db.session.add_all(staffs)
    db.session.add_all(customers)
    db.session.add_all(corporate_customers)

    load_products('products.txt')

    # Add Premade Box Products
    premade_boxes = [
        {'available': True, 'size': 'Small', 'price': 20.00},
        {'available': True, 'size': 'Medium', 'price': 30.00},
        {'available': True, 'size': 'Large', 'price': 40.00},
    ]

    boxes = []
    for box in premade_boxes:
        boxes.append(PremadeBoxProduct(available=box['available'], size=box['size'], price=box['price']))
    db.session.add_all(boxes)
    db.session.commit()

    # Add Box Components (linking vegetables to boxes)
    box_components = [
        {'box_id': boxes[0].id, 'vegetable_id': 7, 'quantity': 2.0},  # Potatoes
        {'box_id': boxes[0].id, 'vegetable_id': 20, 'quantity': 1},  # Cucumber
        {'box_id': boxes[0].id, 'vegetable_id': 2, 'quantity': 1.0},    # Tomatoes
        {'box_id': boxes[0].id, 'vegetable_id': 10, 'quantity': 1},  # Baby Spinach
        {'box_id': boxes[0].id, 'vegetable_id': 18, 'quantity': 1},  # Cauliflower
        {'box_id': boxes[1].id, 'vegetable_id': 6, 'quantity': 1},    # Kumaras
        {'box_id': boxes[1].id, 'vegetable_id': 9, 'quantity': 1},  # Cherry Tomatoes
        {'box_id': boxes[1].id, 'vegetable_id': 21, 'quantity': 2},  # Capsicum
        {'box_id': boxes[1].id, 'vegetable_id': 20, 'quantity': 1},    # Cucumber
        {'box_id': boxes[1].id, 'vegetable_id': 1, 'quantity': 1.5},  # CArrots
        {'box_id': boxes[1].id, 'vegetable_id': 11, 'quantity': 1},  # Lettuce
        {'box_id': boxes[1].id, 'vegetable_id': 3, 'quantity': 1},    # Onions
        {'box_id': boxes[2].id, 'vegetable_id': 6, 'quantity': 1},    # Kumaras
        {'box_id': boxes[2].id, 'vegetable_id': 2, 'quantity': 1.5},  # Tomatoes
        {'box_id': boxes[2].id, 'vegetable_id': 3, 'quantity': 0.5},  # Onions
        {'box_id': boxes[2].id, 'vegetable_id': 7, 'quantity': 2.5},    # Potatoes
        {'box_id': boxes[2].id, 'vegetable_id': 11, 'quantity': 1},  # lettuce
        {'box_id': boxes[2].id, 'vegetable_id': 20, 'quantity': 2},  # cucumber
        {'box_id': boxes[2].id, 'vegetable_id': 16, 'quantity': 1}, # Cabbage
        {'box_id': boxes[2].id, 'vegetable_id': 17, 'quantity': 1},  # Brocolli
        {'box_id': boxes[2].id, 'vegetable_id': 10, 'quantity': 1},  # Baby Spinach
        {'box_id': boxes[2].id, 'vegetable_id': 18, 'quantity': 1} # Cauliflower
    ]

    for component in box_components:
        box_component = BoxComponent(box_id=component['box_id'], vegetable_id=component['vegetable_id'], quantity=component['quantity'])
        db.session.add(box_component)

    # Commit box components to the database
    db.session.commit()

    orders.append(Order( # order 1
        date=datetime(2024, 9, 13, 12, 30), 
        customer_id=4,
        is_delivery=False,
        is_charge_to_account=False,
        status='Completed'))
    
    orders.append(Order( # order 2
        date=datetime(2024, 9, 20, 12, 30),
        customer_id=4,
        is_delivery=False,
        is_charge_to_account=True,
        status='Ready for Pickup'))
    
    orders.append(Order( # order 3
        date=datetime(2024, 9, 30, 10, 30),
        customer_id=4,
        is_delivery=True,
        is_charge_to_account=False,
        status='Confirmed'))
    
    orders.append(Order( # order 4
        date=datetime(2024, 10, 15, 12, 30),
        customer_id=4,
        is_delivery=False,
        is_charge_to_account=True,
        status='Cancelled'))
    
    orders.append(Order( # order 5
        date=datetime(2024, 10, 20, 12, 30),
        customer_id=9,
        is_delivery=False,
        is_charge_to_account=False,
        status='Ready for Pickup'))
    
    orders.append(Order( # order 6
        date=datetime(2024, 10, 20, 10, 30),
        customer_id=5,
        is_delivery=False,
        is_charge_to_account=True,
        status='Confirmed'))
    
    orders.append(Order( # order 7
        date=datetime(2024, 10, 30, 12, 30),
        customer_id=4,
        is_delivery=False,
        is_charge_to_account=False,
        status='Pending'))
    
    orders.append(Order( # order 8
        date=datetime(2024, 11, 1, 12, 30),
        customer_id=4,
        is_delivery=False,
        is_charge_to_account=True,
        status='Ready for Pickup'))
    
    orders.append(Order( # order 9
        date=datetime(2024, 10, 15, 12, 30),
        customer_id=6,
        is_delivery=True,
        is_charge_to_account=False,
        status='Shipped'))
    
    orders.append(Order( # order 10
        date=datetime(2024, 10, 20, 12, 30),
        customer_id=7,
        is_delivery=False,
        is_charge_to_account=False,
        status='Ready for Pickup'))
    
    orders.append(Order( # order 11
        date=datetime(2024, 10, 22, 10, 30),
        customer_id=8,
        is_delivery=False,
        is_charge_to_account=True,
        status='Confirmed'))
    
    orders.append(Order( # order 12
        date=datetime(2024, 10, 25, 10, 30),
        customer_id=9,
        is_delivery=False,
        is_charge_to_account=False,
        status='Pending'))
    
    db.session.add_all(orders)
    
    items.append(WeightedVeggie( # item 1
        name='Carrots',
        price = 1.99,
        weight = 1.0
    ))

    items.append(WeightedVeggie( # item 2
        name='Tomatoes',
        price = 4.99,
        weight = 1.0
    ))

    items.append(WeightedVeggie( # item 3
        name='Gingers',
        price = 9.99,
        weight = 1.0
    ))

    items.append(PremadeBox( # item 4
        size='Small',
        price = 20.00,
        no_of_boxes = 1
    ))

    items.append(WeightedVeggie( # item 5/box 1
        name='Potatoes',
        price = 1.89,
        weight = 2.0,
        premadebox_id=4
    ))

    items.append(UnitPriceVeggie( # item 6/box 1
        name='Cucumber',
        price = 3.99,
        quantity = 1,
        premadebox_id=4
    ))

    items.append(WeightedVeggie( # item 7/box 1
        name='Tomatoes',
        price = 4.99,
        weight = 1.0,
        premadebox_id=4
    ))

    items.append(PackVeggie( # item 8/box 1
        name='Baby Spinach (130g)',
        price = 3.99,
        no_of_pack = 1,
        premadebox_id=4
    ))

    items.append(UnitPriceVeggie( # item 9/box 1
        name='Cauliflower',
        price = 3.99,
        quantity = 1,
        premadebox_id=4
    ))

    items.append(UnitPriceVeggie( # item 10
        name='Cabbage',
        price = 2.89,
        quantity = 1
    ))

    items.append(PackVeggie( # item 11
        name='Baby Spinach (130g)',
        price = 3.99,
        no_of_pack = 10
    ))

    items.append(WeightedVeggie( # item 12
        name='Onions',
        price = 0.99,
        weight = 5.0
    ))

    items.append(WeightedVeggie( # item 13
        name='Kumaras',
        price = 5.99,
        weight = 5.0
    ))

    items.append(UnitPriceVeggie( # item 14
        name='Cucumber',
        price = 3.99,
        quantity = 5
    ))

    items.append(WeightedVeggie( # item 15
        name='Garlics',
        price = 41.99,
        weight = 5.0
    ))

    items.append(WeightedVeggie( # item 16
        name='Onions',
        price = 0.99,
        weight = 15.0
    ))

    items.append(WeightedVeggie( # item 17
        name='Kumaras',
        price = 5.99,
        weight = 5.0
    ))

    items.append(UnitPriceVeggie( # item 18
        name='Cucumber',
        price = 3.99,
        quantity = 5
    ))

    items.append(WeightedVeggie( # item 19
        name='Tomatoes',
        price = 4.99,
        weight = 1.0
    ))

    items.append(PackVeggie( # item 20
        name='Washed Lettuce (250g)',
        price = 5.99,
        no_of_pack = 5
    ))

    db.session.add_all(items)

    orderlines.append(OrderLine(
        order_id=1,
        item_id=1))
    
    orderlines.append(OrderLine(
        order_id=2,
        item_id=2))
    
    orderlines.append(OrderLine(
        order_id=2,
        item_id=3))
    
    orderlines.append(OrderLine(
        order_id=3,
        item_id=4))
    
    orderlines.append(OrderLine(
        order_id=4,
        item_id=10))
    
    orderlines.append(OrderLine(
        order_id=5,
        item_id=11))
    
    orderlines.append(OrderLine(
        order_id=5,
        item_id=12))
    
    orderlines.append(OrderLine(
        order_id=6,
        item_id=13))
    
    orderlines.append(OrderLine(
        order_id=6,
        item_id=14))
    
    orderlines.append(OrderLine(
        order_id=7,
        item_id=15))
    
    orderlines.append(OrderLine(
        order_id=8,
        item_id=16))
    
    orderlines.append(OrderLine(
        order_id=9,
        item_id=17))
    
    orderlines.append(OrderLine(
        order_id=10,
        item_id=18))
    
    orderlines.append(OrderLine(
        order_id=10,
        item_id=19))
    
    orderlines.append(OrderLine(
        order_id=11,
        item_id=20))
    
    db.session.add_all(orderlines)
    
    payments.append(CreditCard(
        order_id=1,
        amount=1.99,
        customer_id=4,
        card_type='Visa',
        card_number='1234567890123456',
        card_expiry='12/25'
    ))

    payments.append(DebitCard(
        order_id=3,
        amount=30.00,
        customer_id=4,
        bank_name='Bank A',
        card_number='1234567890123456'
    ))

    payments.append(CreditCard(
        order_id=5,
        amount=40.37,
        customer_id=9,
        card_type='Mastercard',
        card_number='1234567890123456',
        card_expiry='12/25'
    ))

    payments.append(DebitCard(
        order_id=9,
        amount=39.95,
        customer_id=6,
        bank_name='Bank B',
        card_number='1234567890123456'
    ))

    payments.append(CreditCard(
        order_id=10,
        amount=19.95,
        customer_id=7,
        card_type='Visa',
        card_number='1234567890123456',
        card_expiry='12/25'
    ))

    db.session.add_all(payments)

    # Commit to save data
    db.session.commit()