# grocer

/GROCER/
│
├── app.py
├── connect.py
├── seed.py
├── database.py
├── models/
│   ├── __init__.py
│   ├── person.py
│   ├── staff.py
│   ├── customer.py     # Customer model
│   ├── corporate_customer.py     # Customer model
│   ├── order.py
│   ├── orderline.py
│   ├── payment.py
│   ├── cc_payment.py
│   ├── dc_payment.py
│   ├── item.py
│   ├── vegetable.py
│   ├── weighted_veggie.py
│   ├── pack_veggie.py
│   ├── unit_price_veggie.py
│   ├── premadebox.py
├── routes/
│   ├── __init__.py
│   ├── customer_route.py
│   ├── store_route.py
│   ├── staff_route.py
├── templates/
├── static/
└── tests/                # New test directory
    ├── __init__.py
    ├── test_person.py
    ├── test_staff.py
    ├── test_customer.py
    ├── test_corporate_customer.py
    ├── test_order.py
    ├── test_orderline.py
    ├── test_payment.py
    ├── test_cc_payment.py
    ├── test_dc_payment.py
    ├── test_item.py
    ├── test_vegetable.py
    ├── test_weighted_veggie.py
    ├── test_pack_veggie.py
    ├── test_unit_price_veggie.py
    ├── test_premadebox.py
    ├── test_routes.py