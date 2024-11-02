from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from datetime import datetime
from decorators import role_required
from models import db, Order
from models import DebitCard, CreditCard

payment_bp = Blueprint('payment', __name__)

@payment_bp.route("/<int:order_id>/account_charge", methods=['POST'])
@role_required('customer', 'corporate_customer')
def charge_to_account(order_id):    
    """This route allows the customer to charge their order to their account.

    @param order_id The ID of the order to charge.
    @return Redirect to the customer dashboard.
    """
    payment_type = request.form.get('payment_type')
    if payment_type == 'charge_to_account':
        try:
            order = Order.query.get_or_404(order_id)
            order.charge_to_account()
            db.session.commit()
            flash('Order has been charged to account!', 'success')
            return redirect(url_for('order.view_order', order_id=order_id))
        except Exception as e:
            flash(str(e), 'error')
            db.session.rollback()
            return redirect(url_for('order.check_out', order_id=order_id))
    else:
        flash('Invalid payment type.', 'error')
        return redirect(url_for('order.check_out', order_id=order_id))

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

@payment_bp.route("/payment/<int:order_id>", methods=['POST'])
@role_required('customer', 'corporate_customer')
def card_payment(order_id):    
    """This route processes the customer's payment.
    @return Redirect to the customer dashboard.
    """    
    payment_type = request.form.get('payment_type')

    if payment_type not in ['credit_card', 'debit_card']:
        flash('Invalid payment type.', 'error')
        return redirect(url_for('order.check_out', order_id=order_id))
    
    order = Order.query.get_or_404(order_id)
    amount = order.calculate_final_total()
    customer_id = session['user_id']
    card_no = request.form.get('card_no').replace(' ', '')
    
    if payment_type == 'credit_card':        
        card_type = request.form.get('card_type')
        expiry = request.form.get('expiry')
        cvv = request.form.get('cvv')
        print(card_no, card_type, expiry, cvv)
            
        try:
            is_valid_cc_payment(card_type, card_no, expiry, cvv)
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('order.check_out', order_id=order_id))
    
        # Create a new credit card payment            
        payment = CreditCard(
            card_type=card_type, 
            card_number=card_no, 
            card_expiry=expiry,
            amount=amount,
            customer_id=customer_id,
            order_id=order_id
        )          
        
    elif payment_type == 'debit_card':
        card_no = request.form.get('card_no').replace(' ', '')
        bank = request.form.get('bank')

        try:
            is_valid_dc_payment(bank, card_no)
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('order.check_out', order_id=order_id))
                
        # Create a new debit card payment
        payment = DebitCard(
            bank_name=bank, 
            card_number=card_no, 
            amount=amount,
            customer_id=customer_id,
            order_id=order_id,
        )

    try:
        db.session.add(payment) 

        # Ensure payment is added to the database before updating order
        db.session.flush()

        if payment.id:  
            order.confirm_order()
            db.session.commit()
            flash('Payment successful!', 'success')
            return redirect(url_for('order.view_order', order_id=order_id))
        else:
            raise Exception('Payment failed. Please try again.')  
    except Exception as e:
        db.session.rollback()
        flash(str(e), 'error')        
        return redirect(url_for('order.check_out', order_id=order_id)) 
    
@payment_bp.route("/account_payment", methods=['GET', 'POST'])
@role_required('customer', 'corporate_customer')
def account_payment():
    """This route processes the customer's payment for outstanding balance in account.
    @return Redirect to the customer profile.
    """    
    pass