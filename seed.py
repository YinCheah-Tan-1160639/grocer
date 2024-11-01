from database import db

from models import Staff, vegetable
from models import Customer
from models import CorporateCustomer
from models import Order
from models import OrderLine
from models import PackVeggie
from models import WeightedVeggie
# from models.product import Product
from models import UnitPriceVeggie
from models.product import VegetableProduct
from models.product import PremadeBoxProduct
from models.product import BoxComponent
# from models import Payment

# Load and parse a text file to create product objects
def load_products(txt_file):
    with open(txt_file, 'r') as file:
        products = []
        for line in file:
            product = line.strip().split(', ')
            if len(product) != 4:  # Ensure there are exactly 4 fields
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

def insert_test_data():
    # Create sample data

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

    # orders.append(Order(
    #     customer_id=4,
    #     is_delivery=False,
    #     is_confirmed=True,
    #     is_charge_to_account=False,
    #     status='Paid'))

    # # orderlines.append(OrderLine(
    # #     order_id=1)) 
    
    # items.append(WeightedVeggie(
    #     name='Carrots',
    #     price = 1.99,
    #     weight = 0.5
    # ))

    # orderlines.append(OrderLine(
    #     order_id=1,
    #     item_id=1))
    
    # orderline_items.append(PackVeggie(
    #     orderline_id=2,
    #     name='Baby Spinach (130g)',
    #     price = 3.99,
    #     no_of_pack = 2
    # ))

    # orderlines.append(OrderLine(
    #     order_id=1))
    
    # orderline_items.append(UnitPriceVeggie(
    #     orderline_id=3,
    #     name='Cabbage',
    #     price = 2.89,
    #     quantity = 1
    # ))

    # orderlines.append(OrderLine(
    #     order_id=1))
    
    # orderline_items.append(WeightedVeggie(
    #     orderline_id=4,
    #     name='Tomatoes',
    #     price = 4.99,
    #     weight = 1.2
    # ))  
    
    # orders.append(Order(
    #     customer_id=4))
    
    # orderlines.append(OrderLine(
    #     order_id=2))
    
    # orderline_items.append(WeightedVeggie(
    #     orderline_id=5,
    #     name='Gingers',
    #     price = 9.99,
    #     weight = 0.2
    # ))

    # orderlines.append(OrderLine(
    #     order_id=2))
    
    # orderline_items.append(PackVeggie(
    #     orderline_id=6,
    #     name='Washed Lettuce (250g)',
    #     price = 5.99,
    #     no_of_pack = 1
    # ))
    
    # orders.append(Order(
    #     customer_id=5))
    
    # orderlines.append(OrderLine(
    #     order_id=3))
    
    # orderline_items.append(WeightedVeggie(
    #     orderline_id=7,
    #     name='Onions',
    #     price = 0.99,
    #     weight = 0.3
    # ))
    
    # orders.append(Order(
    #     customer_id=7))
    
    # orderlines.append(OrderLine(
    #     order_id=4))
    
    # orderline_items.append(PackVeggie(
    #     orderline_id=8,
    #     name='Shredded Cabbage (200g)',
    #     price = 3.99,
    #     no_of_pack = 1
    # ))

    # orderlines.append(OrderLine(
    #     order_id=4))
    
    # orderline_items.append(UnitPriceVeggie(
    #     orderline_id=9,
    #     name='Brocolli',
    #     price = 1.99,
    #     quantity = 1
    # ))

    # orderlines.append(OrderLine(
    #     order_id=4))
    
    # orderline_items.append(WeightedVeggie(
    #     orderline_id=10,
    #     name='Kumaras',
    #     price = 5.99,
    #     weight = 2.0
    # ))  

    

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

    # db.session.add_all(orders)
    # db.session.add_all(items)
    # db.session.add_all(orderlines)
    

    # Commit to save data
    db.session.commit()