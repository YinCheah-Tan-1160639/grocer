from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from datetime import datetime
from decorators import role_required
from models import db, Order, OrderLine, Product, WeightedVeggie, PackVeggie, UnitPriceVeggie, Customer
from models.premadebox import PremadeBox

order_bp = Blueprint('order', __name__, url_prefix='/order')

def create_vegetable_item(name, price, qty, unit, premadebox_id=None):
    if unit == 'kg':
        return WeightedVeggie(name=name, price=price, weight=qty, premadebox_id=premadebox_id)
    elif unit == 'pack':
        return PackVeggie(name=name, price=price, no_of_pack=qty, premadebox_id=premadebox_id)
    elif unit == 'each':
        return UnitPriceVeggie(name=name, price=price, quantity=qty, premadebox_id=premadebox_id)
    else:
        raise ValueError("Invalid unit type")

@order_bp.route("/new", methods=['GET','POST'])
@role_required('customer', 'corporate_customer')
def create_order():
    """This route allows the customer to initiate an order process.
    @return Redirect to the order page.
    """
    veggies = Product().get_available_vegetables()
    boxes = Product().get_available_premade_boxes()

    if request.method == 'GET':
        customer = Customer.query.get_or_404(session['user_id'])
        if customer.can_place_order():
            return render_template("customer/order/create.html", veggies=veggies, boxes=boxes, role=session['role'])
        return render_template("customer/order/list.html", veggies=veggies, boxes=boxes, role=session['role'])
    else:
        new_order = Order(customer_id=session['user_id'])
        db.session.add(new_order)
        db.session.commit()

        # Process vegetables quantities in the form
        for veggie in veggies:
            veggie_name = veggie['name']
            veggie_price = veggie['price']
            veggie_unit = veggie['unit']

            # Check if weight or quantity is provided
            if request.form.get(veggie_name):
                # Handle weighted vegetables
                qty = Decimal(request.form.get(veggie_name))

                if qty > 0:
                    veggie_item = create_vegetable_item(veggie_name, veggie_price, qty, veggie_unit)
                    db.session.add(veggie_item)
                    db.session.commit()

                    order_line = OrderLine(order_id=new_order.id, item_id=veggie_item.id)
                    db.session.add(order_line)
                    db.session.commit()

        # Process premade boxes quantities in the form
        for box in boxes:
            box_size = box['size']
            box_price = box['price']

            if request.form.get(box_size):
                box_qty = int(request.form.get(box_size))

                if box_qty > 0:
                    premadebox_item = PremadeBox(size=box_size, price=box_price, no_of_boxes=box_qty)
                    db.session.add(premadebox_item)
                    order_line = OrderLine(order_id=new_order.id, item_id=premadebox_item.id)
                    db.session.add(order_line)
                    db.session.commit()
                    for content in box['contents']:
                        content_item = create_vegetable_item(content['product']['name'], content['product']['price'], content['quantity'], content['product']['unit'], premadebox_item.id)
                        db.session.add(content_item)
                        db.session.commit()

        # Commit all changes to the database
        db.session.commit()
                        
        # Confirm to the user and redirect
        flash('Order has been successfully created!', 'success')
        return redirect(url_for('order.confirm_order', order_id=new_order.id))
    
    # try:
    #     # Create order process
    #     pass
    # except Exception as e:
    #     flash(str(e), 'error')
    #     return redirect(url_for('store.dashboard'))
    # return redirect(url_for('store.dashboard'))

@order_bp.route("/confirm_order/<int:order_id>", methods=['GET', 'POST'])
@role_required('customer', 'corporate_customer')
def confirm_order(order_id):    
    """
    Confirm the customer's order.
    This route processes the customer's order and confirms the order details.

    @param order_id The ID of the order to confirm.
    @return Redirect to payment.
    """
    order = Order.query.get_or_404(order_id)
    total_amount = order.calculate_total()

    if request.method == 'GET':
        # For GET request, display the order confirmation details
        return render_template('customer/order/confirm.html', 
                            order=order,
                            total=total_amount, 
                            role=session['role'], 
                            user_id=session['user_id'])
    else:
        # For POST request, process the order confirmation
        order.confirm_order()
        db.session.commit()
        return redirect(url_for('customer.check_out', order_id=order_id))