from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from decorators import role_required
from models import db, Order, OrderLine, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox
from models import PremadeBoxProduct
from models import VegetableProduct
from models import DebitCard, CreditCard
from models.corporate_customer import CorporateCustomer

order_bp = Blueprint('order', __name__, url_prefix='/order')

@order_bp.route("/new", methods=['GET','POST'])
@role_required('customer', 'corporate_customer')
def create_order():
    """This route allows the customer to initiate an order process.
    @return Redirect to the order page.
    """    
    unit_veggies = VegetableProduct.query.filter_by(available=True, unit="each").order_by(VegetableProduct.name).all()
    pack_veggies = VegetableProduct.query.filter_by(available=True, unit="pack").order_by(VegetableProduct.name).all()
    weight_veggies = VegetableProduct.query.filter_by(available=True, unit="kg").order_by(VegetableProduct.name).all()
    boxes = PremadeBoxProduct.query.filter_by(available=True).all()
    
    if request.method == 'GET':

        return render_template("customer/order/new.html", 
                            unit_veggies=unit_veggies,
                            pack_veggies=pack_veggies,
                            weight_veggies=weight_veggies, 
                            boxes=boxes, 
                            role=session['role']
                            )
    else:
        w_veggies = {}
        p_veggies = {}
        u_veggies = {}
        p_boxes = {}
    
        # Iterate through the form data
        for key in request.form:
            if key.startswith('weight_'):
                item_id = int(key.split('_')[1])  # Extract the item ID from the key
                weight = request.form.get(key)  # Get the weight value
                if weight:  # Ensure the weight is not empty
                    try:
                        weight = float(weight)  # Convert the weight to a float
                    except ValueError:
                        flash(f"Invalid weight for item {item_id}", 'error')
                        return redirect(url_for('order.create_order'))
                    w_veggies[item_id] = weight

            elif key.startswith('pack_'):
                item_id = int(key.split('_')[1])  # Extract the item ID from the key 
                pack = request.form.get(key)  # Get the pack value
                if pack and pack.isdigit():  # Ensure the pack is not empty
                    try:
                        pack = int(pack)  # Convert the pack to an integer
                    except ValueError:
                        flash(f"Invalid pack for item {item_id}", 'error')
                        return redirect(url_for('order.create_order'))
                    p_veggies[item_id] = pack

            elif key.startswith('unit_'):
                item_id = int(key.split('_')[1])
                unit = request.form.get(key)
                if unit and unit.isdigit():
                    try:
                        unit = int(unit)
                    except ValueError:
                        flash(f"Invalid unit for item {item_id}", 'error')
                        return redirect(url_for('order.create_order'))
                    u_veggies[item_id] = unit

            elif key.startswith('box_'):
                item_id = int(key.split('_')[1])
                box = request.form.get(key)
                if box and box.isdigit():
                    try:
                        box = int(box)
                    except ValueError:
                        flash(f"Invalid box for item {item_id}", 'error')
                        return redirect(url_for('order.create_order'))
                    p_boxes[item_id] = box
            
            else:
                flash(f"Invalid Item: {key}", 'error')
                return redirect(url_for('order.create_order'))
        print(w_veggies, p_veggies, u_veggies, p_boxes)

        if all(not item for item in (w_veggies, p_veggies, u_veggies, p_boxes)):
            flash("No items selected for order", 'error')
            return redirect(url_for('order.create_order'))
        
        new_order = Order(customer_id=session['user_id'])
        db.session.add(new_order)
        db.session.commit()

        # Process the quantities
        if w_veggies:  # Check if there are any quantities to process
            for item_id, weight in w_veggies.items():                
                item = VegetableProduct.query.get(item_id)
                print(item)
                veggie_item = WeightedVeggie(name=item.name, price=item.price, weight=weight)
                db.session.add(veggie_item)
                db.session.commit()
                order_line = OrderLine(order_id=new_order.id, item_id=veggie_item.id) 
                db.session.add(order_line)
                db.session.commit()

        if p_veggies:
            for item_id, pack in p_veggies.items():
                item = VegetableProduct.query.get(item_id)
                veggie_item = PackVeggie(name=item.name, price=item.price, no_of_pack=pack)
                db.session.add(veggie_item)
                db.session.commit()
                order_line = OrderLine(order_id=new_order.id, item_id=veggie_item.id)
                db.session.add(order_line)
                db.session.commit()

        if u_veggies:
            for item_id, unit in u_veggies.items():
                item = VegetableProduct.query.get(item_id)
                veggie_item = UnitPriceVeggie(name=item.name, price=item.price, quantity=unit)
                db.session.add(veggie_item)
                db.session.commit()
                order_line = OrderLine(order_id=new_order.id, item_id=veggie_item.id)
                db.session.add(order_line)
                db.session.commit()

        if p_boxes:
            for item_id, box in p_boxes.items():
                item = PremadeBoxProduct.query.get(item_id)
                premadebox_item = PremadeBox(size=item.size, price=item.price, no_of_boxes=box)
                db.session.add(premadebox_item)
                db.session.commit()
                order_line = OrderLine(order_id=new_order.id, item_id=premadebox_item.id)
                db.session.add(order_line)
                db.session.commit()
                for component in item.components:
                    if component.vegetable.unit == 'kg':
                        content_item = WeightedVeggie(name=component.vegetable.name, price=component.vegetable.price, weight=component.quantity, premadebox_id=premadebox_item.id)
                    elif component.vegetable.unit == 'pack':
                        content_item = PackVeggie(name=component.vegetable.name, price=component.vegetable.price, no_of_pack=component.quantity, premadebox_id=premadebox_item.id)
                    elif component.vegetable.unit == 'each':
                        content_item = UnitPriceVeggie(name=component.vegetable.name, price=component.vegetable.price, quantity=component.quantity, premadebox_id=premadebox_item.id)
                    db.session.add(content_item)
                    db.session.commit()

        # Confirm to the user and redirect
        flash('Order has been successfully created!', 'success')
        return redirect(url_for('order.confirm_order', order_id=new_order.id))

@order_bp.route("/confirm_order/<int:order_id>", methods=['GET', 'POST'])
@role_required('customer', 'corporate_customer')
def confirm_order(order_id):    
    """This route allow customer to review their order, select delivery options and confirm their order.

    @param order_id The ID of the order to confirm.
    @return Redirect to payment.
    """
    order = Order.query.get_or_404(order_id)    
    if not order:
        flash("Order not found.", "error")
        return redirect(url_for('order.create_order'))
    
    if request.method == 'GET':
        # For GET request, display the order confirmation details
        total_amount = order.calculate_total()
        discount = 0
        if session['role'] == 'corporate_customer':
            total_amount = order.calculate_corporate_total()
            discount = order.calculate_discount()

        if total_amount == 0:
            flash("No items in the order.", "error")
            return redirect(url_for('order.create_order'))
    
        return render_template('customer/order/confirm.html', 
                            order=order,
                            total=total_amount, 
                            discount=discount,
                            role=session['role'], 
                            user_id=session['user_id'])
    else:
        # For POST request, process delivery if delivery selected
        if request.form.get('delivery'):
            order.require_delivery()

            db.session.commit()
            print(order.is_delivery)
        return redirect(url_for('order.check_out', order_id=order_id))
    
@order_bp.route("/check_out/<int:order_id>")
@role_required('customer', 'corporate_customer')
def check_out(order_id):    
    """This route allows the customer to proceed to payment.
    @return Rendered HTML template for the payment.
    """
    order = Order.query.get_or_404(order_id)
    total_amount = order.calculate_final_total()
    banks = DebitCard.VALID_BANKS
    card_types = CreditCard.VALID_CARD_TYPES
    return render_template("customer/payment.html", 
                           role=session['role'], 
                           order_id=order_id, 
                           total=total_amount,
                           banks=banks,
                           card_types=card_types)

@order_bp.route("/list")
@role_required('customer', 'corporate_customer')
def list_orders():
    """This route renders the orders associated with the customer,
    allowing them to view their order history.

    @return Rendered HTML template showing the list of orders.
    """
    orders = Order.query.filter_by(customer_id=session['user_id']).order_by(Order.date.desc()).all()
    if not orders:
        flash("No orders found.", "error")
    return render_template("customer/order/list.html", orders=orders, role=session['role'])   

@order_bp.route("/order/<int:order_id>")
@role_required('customer', 'corporate_customer')
def view_order(order_id):    
    """This route retrieves a specific order and renders the order details
    in the customer view.

    @param order_id The ID of the order to view.
    @return Rendered HTML template showing the order details.
    """
    order = Order.query.get_or_404(order_id)
    if not order:
        flash("Order not found.", "error")
        return redirect(url_for('order.list_orders'))
    if order.customer_id != session['user_id']:
        flash("You are not authorized to view this order.", "error")
        return redirect(url_for('order.list_orders'))
    total, discount, delivery_fee = order.private_total_display()
    if isinstance (order.customer, CorporateCustomer):
        total, discount, delivery_fee = order.corporate_total_display()
    return render_template("customer/order/view.html", 
                            order=order,
                            total=total,
                            delivery_fee=delivery_fee,
                            discount=discount, 
                            role=session['role'], 
                            user_id=session['user_id']
                            )


@order_bp.route("/cancel_order/<int:order_id>", methods=['POST'])
@role_required('customer', 'corporate_customer')
def cancel_order(order_id):    
    """This route allows the customer to cancel a specific order if order hasn't been fulfilled.

    @param order_id The ID of the order to cancel.
    @return Redirect to the order view.
    """
    order = Order.query.get_or_404(order_id)
    print(order.status)
    if not order:
        flash("Order not found.", "error")
        return redirect(url_for('order.list_orders'))
    if order.customer_id != session['user_id']:
        flash("You are not authorized to cancel this order.", "error")
        return redirect(url_for('order.list_orders'))
    try:
        order.cancel_order()
        db.session.commit()
        flash("Order has been successfully cancelled.", "success")
    except ValueError as e:
        flash(str(e), "error")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for('order.view_order', order_id=order.id))

    # def create_vegetable_item(name, price, qty, unit, premadebox_id=None):
    # if unit == 'kg':
    #     return WeightedVeggie(name=name, price=price, weight=qty, premadebox_id=premadebox_id)
    # elif unit == 'pack':
    #     return PackVeggie(name=name, price=price, no_of_pack=qty, premadebox_id=premadebox_id)
    # elif unit == 'each':
    #     return UnitPriceVeggie(name=name, price=price, quantity=qty, premadebox_id=premadebox_id)
    # else:
    #     raise ValueError("Invalid unit type")
                        