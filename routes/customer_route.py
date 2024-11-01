# This file contains the routes for the customer view.
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from datetime import datetime
from decorators import role_required
from models import Person
from app import db
from models import Order
from models import CreditCard
from models import DebitCard
from models.product import PremadeBoxProduct, VegetableProduct

customer_bp = Blueprint('customer', __name__)

@customer_bp.route("/profile")
@role_required('customer', 'corporate_customer')
def profile():
    user = Person.query.get_or_404(session['user_id'])
    return render_template("customer/profile.html", 
                           role=session['role'],
                           username=session['username'],
                           user=user) 


@customer_bp.route("/veggies")
@role_required('customer', 'corporate_customer')
def list_veggies():
    """This route retrieves a list of vegetables that are available for
    customers and renders them in the customer view.

    @return Rendered HTML template showing the list of available vegetables.
    """
    try:
        veggies = VegetableProduct.query.filter_by(available=True).all()
        if not veggies:
            flash("No available vegetables found.", 'warning')
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('store.index'))   
    return render_template("customer/list_veggies.html", veggies=veggies, role=session['role'])

@customer_bp.route("/premade_boxes")
@role_required('customer', 'corporate_customer')
def list_premade_boxes():
    """This route retrieves a list of premade boxes that are available for
    customers and renders them in the customer view.

    @return Rendered HTML template showing the list of available premade boxes.
    """

    try:
        boxes = PremadeBoxProduct.query.filter_by(available=True).all()
        if not boxes:
            flash("No available premade boxes found.", 'warning')
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('store.dashboard'))   
    return render_template("customer/list_premadeboxes.html", boxes=boxes, role=session['role'])

    



#     # try:
#     #     # Confirm order process
#     #     pass
#     # except Exception as e:
#     #     flash(str(e), 'error')
#     #     return redirect(url_for('store.dashboard'))
#     # return redirect(url_for('store.dashboard'))

@customer_bp.route("/check_out/<int:order_id>")
@role_required('customer', 'corporate_customer')
def check_out(order_id):    
    """
    Checkout the customer's order.

    This route allows the customer to proceed to payment.

    @return Rendered HTML template for the checkout process.
    """
    order = Order.query.get_or_404(order_id)
    total_amount = order.calculate_total()
    banks = DebitCard.VALID_BANKS
    card_types = CreditCard.VALID_CARD_TYPES
    return render_template("customer/checkout.html", 
                           role=session['role'], 
                           order=order, 
                           total=total_amount,
                           banks=banks,
                           card_types=card_types)
#     # try:
#     #     # Checkout process
#     #     pass
#     # except Exception as e:
#     #     flash(str(e), 'error')
#     #     return redirect(url_for('store.dashboard'))
#     # return render_template("customer/checkout.html", role=session['role'])

@customer_bp.route("/charge_to_account/<int:order_id>", methods=['POST'])
@role_required('customer', 'corporate_customer')
def charge_to_account(order_id):    
    """
    Charge the customer's order to their account.

    This route allows the customer to charge their order to their account.

    @param order_id The ID of the order to charge.
    @return Redirect to the customer dashboard.
    """
    payment_type = request.form.get('payment_type')
    if payment_type == 'charge_to_account':
        try:
            order = Order.query.get_or_404(order_id)
            order.charge_to_account()
            amount = order.calculate_total()
            order.customer.update_balance(amount)
            db.session.commit()
            flash('Order has been charged to account!', 'success')
            return redirect(url_for('customer.view_order', order_id=order_id))
        except Exception as e:
            flash(str(e), 'error')
            db.session.rollback()
            return redirect(url_for('customer.check_out', order_id=order_id))
    else:
        flash('Invalid payment type.', 'error')
        return redirect(url_for('customer.check_out', order_id=order_id))

def is_valid_cvv(cvv: str) -> bool:
    """! To validate the CVV of the credit card.
    @return A boolean value indicating the CVV is valid.
    """
    if not cvv.isdigit() or len(cvv) != 3:
        raise ValueError("Invalid CVV. Must be 3 digits.")
    return True

def is_valid_card_number(card_number: str) -> bool:
    """! To validate the credit card number.
    @return A boolean value indicating the credit card number is valid.
    """
    if not card_number:
        raise ValueError("Card number is required.")
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Invalid card number. Must be 16 digits.")
    return True

def is_valid_expiry(card_expiry: str) -> bool:
    """! To validate the expiry date of credit card.
    @return A boolean value indicating the expiry date is valid.
    """
    if not card_expiry:
        raise ValueError("Expiry date is required.")
    try:
        # Parse the expiry date
        expiry_month, expiry_year = card_expiry.split('/')
        expiry_month = int(expiry_month)
        expiry_year = int(expiry_year)
        expiry_date = datetime(year=2000 + expiry_year, month=expiry_month, day=1)  # Use 1st of the month for comparison
        if expiry_date <= datetime.now():
            raise ValueError("Card expiry date is invalid or expired.")
        return True
    except ValueError:
        raise ValueError("Invalid expiry.")
    
def is_valid_card_type(card_type: str) -> bool:
    """! To validate the card type.
    @return A boolean value indicating the card type is valid.
    """
    if not card_type:
        raise ValueError("Card type is required.")
    if card_type not in CreditCard.VALID_CARD_TYPES:
        raise ValueError(f"Invalid card type. Must be one of: {', '.join(CreditCard.VALID_CARD_TYPES)}.")
    return True

def is_valid_bank(bank: str) -> bool:
    """! To validate the bank name.
    @return A boolean value indicating the bank name is valid.
    """
    if not bank:
        raise ValueError("Bank name is required.")
    if bank not in DebitCard.VALID_BANKS:
        raise ValueError(f"Invalid bank name. Must be one of: {', '.join(CreditCard.VALID_BANKS)}.")
    return True

def is_valid_cc_payment(card_type: str, card_number: str, expiry: str, cvv: str) -> bool:
    """! To validate the payment input from the form.
    @return A boolean value indicating the payment is successful.
    """        
    is_valid_card_type(card_type)
    is_valid_card_number(card_number)
    is_valid_expiry(expiry)
    is_valid_cvv(cvv)
    return True

def is_valid_dc_payment(bank: str, card_number: str) -> bool:
    """! To validate the payment input from the form.
    @return A boolean value indicating the payment is successful.
    """        
    is_valid_bank(bank)
    is_valid_card_number(card_number)
    return True

@customer_bp.route("/payment/<int:order_id>", methods=['POST'])
@role_required('customer', 'corporate_customer')
def payment(order_id):    
    """
    Process the customer's payment.
    This route processes the customer's payment.
    @return Redirect to the customer dashboard.
    """    

    payment_type = request.form.get('payment_type')

    if payment_type not in ['credit_card', 'debit_card']:
        flash('Invalid payment type.', 'error')
        return redirect(url_for('customer.check_out', order_id=order_id))
    
    order = Order.query.get_or_404(order_id)
    amount = order.calculate_total()
    
    if payment_type == 'credit_card':
        card_no = request.form.get('card_no').replace(' ', '')
        card_type = request.form.get('card_type')
        # card_type = 'Visa'
        expiry = request.form.get('expiry')
        cvv = request.form.get('cvv')
        print(card_no, card_type, expiry, cvv)
            
        try:
            is_valid_cc_payment(card_type, card_no, expiry, cvv)
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('customer.check_out', order_id=order_id))
        
        try: 
            # Create a new credit card payment
            customer_id = session['user_id']
            payment = CreditCard(
                card_type=card_type, 
                card_number=card_no, 
                card_expiry=expiry,
                amount=amount,
                customer_id=customer_id,
                order_id=order_id
            )
            db.session.add(payment) 

            # Ensure payment is added to the database before updating order
            db.session.flush()  # Flush sends pending changes to the database

            if payment.id:  
                order.update_status('Paid')
                db.session.commit()
                flash('Payment successful!', 'success')
                return redirect(url_for('customer.view_order', order_id=order_id))
            else:
                raise Exception('Payment failed. Please try again.')

        except Exception as e:
            flash(str(e), 'error')
            db.session.rollback()
            return redirect(url_for('customer.check_out', order_id=order_id))
        
    elif payment_type == 'debit_card':
        card_no = request.form.get('card_no').replace(' ', '')
        bank = request.form.get('bank')

        try:
            is_valid_dc_payment(bank, card_no)
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('customer.check_out', order_id=order_id))
        
        try:
            # Create a new debit card payment
            customer_id = session['user_id']
            payment = DebitCard(
                bank_name=bank, 
                card_number=card_no, 
                amount=amount,
                customer_id=customer_id,
                order_id=order_id,
            )
            db.session.add(payment) 

            # Ensure payment is added to the database before updating order
            db.session.flush()  # Flush sends pending changes to the database

            if payment.id:  
                order.update_status('Paid')
                db.session.commit()
                flash('Payment successful!', 'success')
                return redirect(url_for('customer.view_order', order_id=order_id))
            else:
                raise Exception('Payment failed. Please try again.')
            
        except Exception as e:
            flash(str(e), 'error')
            db.session.rollback()
            return redirect(url_for('customer.check_out', order_id=order_id))
        
@customer_bp.route("/list_orders")  
@role_required('customer', 'corporate_customer')
def list_orders():
    """
    List all orders for the logged-in customer.

    This route renders the orders associated with the customer,
    allowing them to view their order history.

    @return Rendered HTML template showing the list of orders.
    """
    try:
        customer = Person.query.get_or_404(session['user_id'])
        orders = customer.orders
        if not orders:
            flash("No orders found.", 'warning')
    except Exception as e:
        flash(str(e), 'error')
    return render_template("customer/order/list.html", orders=orders, role=session['role'])      

@customer_bp.route("/order/<int:order_id>")
@role_required('customer', 'corporate_customer')
def view_order(order_id):    
    """
    View a specific order.

    This route retrieves a specific order and renders the order details
    in the customer view.

    @param order_id The ID of the order to view.
    @return Rendered HTML template showing the order details.
    """

    order = Order.query.get_or_404(order_id)
    
    return render_template("customer/order/view.html", order=order, role=session['role'], user_id=session['user_id'])

    # check if the customer id is the same as the logged in user
    # try:        
    #     order = Customer.get_order_details(order_id)
    # except Exception as e:
    #     flash(str(e), "error")
    #     return redirect(url_for("store.dashboard"))

@customer_bp.route("/cancel_order/<int:order_id>")
@role_required('customer', 'corporate_customer')
def cancel_order(order_id):    
    """
    Cancel a specific order.

    This route allows the customer to cancel a specific order.

    @param order_id The ID of the order to cancel.
    @return Redirect to the customer dashboard.
    """
    pass

    
    # Validate the payment
    # try:
    #     # Payment process
    #     pass
    # except Exception as e:
    #     flash(str(e), 'error')
    #     return redirect(url_for('store.dashboard'))
    # return redirect(url_for('store.dashboard'))

# # Creating a Credit Card payment instance
# def create_credit_card_payment(card_type, card_number, expiry, amount, customer_id):
#     try:
#         # Validate the payment details
#         int(customer_id)
#         # Create an instance, passing parameters for validation
#         payment = CreditCard(
#             card_type=card_type, 
#             card_number=card_number, 
#             card_expiry=expiry,
#             amount=amount,
#             customer_id=customer_id,
#         )
#         db.session.add(payment)
#         db.session.commit()
#         return payment  # Return the payment instance

#     except (ValueError) as e:
#         flash(f'Validation Error: {str(e)}', 'error')
#         db.session.rollback()
#         return None
#     except Exception as e:
#         flash('An error occurred while processing your payment.', 'error')
#         db.session.rollback()
#         return None  # Return None to indicate failure


# @customer_bp.route("/orders")
# @role_required('customer', 'corporate_customer')
# def list_orders():    
#     """
#     List all orders for the logged-in customer.

#     This route renders the orders associated with the customer,
#     allowing them to view their order history.

#     @return Rendered HTML template showing the list of orders.
#     """
#     return render_template("customer/list_orders.html", role=session['role'])

    # try:
    #     # Cancel order process
    #     pass
    # except Exception as e:
    #     flash(str(e), 'error')
    #     return redirect(url_for('store.dashboard'))
    # return redirect(url_for('store.dashboard'))


# veggie_weight = Decimal(request.form.get(veggie_name))
            #     if veggie_weight > 0:
            #         order_line = OrderLine(order_id=new_order.id)
            #         item = WeightedVeggie(
            #             orderline_id=order_line.id, 
            #             name=veggie_name,
            #             price_per_kg=veggie_price,
            #             weight=veggie_weight)
            #         db.session.add(item)
            # elif request.form.get(veggie_name) and veggie_unit == 'pack':
            #     # Handle pack/unit vegetables
            #     veggie_qty = int(request.form.get(veggie_name))
            #     if veggie_qty > 0:
            #         order_line = OrderLine(order_id=new_order.id)
            #         item = PackVeggie(
            #             orderline_id=order_line.id, 
            #             name=veggie_name,
            #             price=veggie_price,
            #             quantity=veggie_qty)
            #         db.session.add(item)
            # elif request.form.get(veggie_name) and veggie_unit == 'each':
            #     # Handle pack/unit vegetables
            #     veggie_qty = int(request.form.get(veggie_name))
            #     if veggie_qty > 0:
            #         order_line = OrderLine(order_id=new_order.id)
            #         item = UnitPriceVeggie(
            #             orderline_id=order_line.id, 
            #             name=veggie_name,
            #             price=veggie_price,
            #             quantity=veggie_qty)
            #         db.session.add(item)
        

        # if veggie_unit == 'kg':
        #                 item = WeightedVeggie(
        #                     orderline_id=order_line.id, 
        #                     name=veggie_name,
        #                     price_per_kg=veggie_price,
        #                     weight=qty)
        #                 db.session.add(item)
        #             elif veggie_unit == 'pack':
        #                 item = PackVeggie(
        #                     orderline_id=order_line.id, 
        #                     name=veggie_name,
        #                     price=veggie_price,
        #                     quantity=qty)
        #                 db.session.add(item)
        #             elif veggie_unit == 'each':
        #                 item = UnitPriceVeggie(
        #                     orderline_id=order_line.id, 
        #                     name=veggie_name,
        #                     price=veggie_price,
        #                     quantity=qty)
        #                 db.session.add(item)

        
            
    #         # Check if weight or quantity is provided
    #         if request.form.get(f"veggie_weight_{veggie_name}"):
    #             # Handle weighted vegetables
    #             veggie_weight = float(request.form.get(f"veggie_weight_{veggie_name}"))
    #             if veggie_weight > 0:  # Only add if quantity is non-zero
    #                 order_line = OrderLine(order_id=new_order.id, item_type="Vegetable", item_name=veggie_name,
    #                                        quantity=veggie_weight, price=veggie_price * veggie_weight)
    #                 db.session.add(order_line)
    #         elif request.form.get(f"veggie_qty_{veggie_name}"):
    #             # Handle pack/unit vegetables
    #             veggie_qty = int(request.form.get(f"veggie_qty_{veggie_name}"))
    #             if veggie_qty > 0:  # Only add if quantity is non-zero
    #                 order_line = OrderLine(order_id=new_order.id, item_type="Vegetable", item_name=veggie_name,
    #                                        quantity=veggie_qty, price=veggie_price * veggie_qty)
    #                 db.session.add(order_line)