from flask import Blueprint, render_template, abort, request, redirect, session, url_for, flash
from decorators import role_required
from models import Customer, Person, Vegetable
from models import Product

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
    """
    List all available vegetables for customers.

    This route retrieves a list of vegetables that are available for
    customers and renders them in the customer view.

    @return Rendered HTML template showing the list of available vegetables.
    """
    try:
        veggies = Product().get_available_vegetables()
        if not veggies:
            flash("No available vegetables found.", 'warning')
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('store.dashboard'))   
    return render_template("customer/list_veggies.html", veggies=veggies, role=session['role'])

@customer_bp.route("/premade_boxes")
@role_required('customer', 'corporate_customer')
def list_premade_boxes():
    """
    List all available premade boxes for customers.

    This route retrieves a list of premade boxes that are available for
    customers and renders them in the customer view.

    @return Rendered HTML template showing the list of available premade boxes.
    """
    try:
        boxes = Product().get_available_premade_boxes()
        if not boxes:
            flash("No available premade boxes found.", 'warning')
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('store.dashboard'))   
    return render_template("customer/list_premadeboxes.html", boxes=boxes, role=session['role'])


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