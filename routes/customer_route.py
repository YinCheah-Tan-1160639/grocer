# This file contains the routes for the customer view.
from flask import Blueprint, render_template, redirect, session, url_for, flash
from decorators import role_required
from models import Customer, PremadeBoxProduct, VegetableProduct

customer_bp = Blueprint('customer', __name__)

@customer_bp.route("/profile")
@role_required('customer', 'corporate_customer')
def profile():
    """This route retrieves the profile of the logged-in customer and renders it.
    
    @return Rendered HTML template showing the customer profile.
    """
    user = Customer.query.get_or_404(session['user_id'])
    return render_template("customer/profile.html", 
                           role=session['role'],
                           username = session['username'],
                           user=user
                           ) 

@customer_bp.route("/veggies")
@role_required('customer', 'corporate_customer')
def list_veggies():
    """This route retrieves a list of vegetables that are available for
    customers and renders them in the customer view.

    @return Rendered HTML template showing the list of available vegetables.
    """
    
    veggies = VegetableProduct.query.filter_by(available=True).order_by(VegetableProduct.name).all()
    if not veggies:
        flash("No available vegetables found.", 'warning')
  
    return render_template("veggie/list.html", veggies=veggies, role=session['role'])

@customer_bp.route("/premade_boxes")
@role_required('customer', 'corporate_customer')
def list_premade_boxes():
    """This route retrieves a list of premade boxes that are available for
    customers and renders them in the customer view.

    @return Rendered HTML template showing the list of available premade boxes.
    """

    boxes = PremadeBoxProduct.query.filter_by(available=True).all()
    if not boxes:
        flash("No available premade boxes found.", 'warning')
    return render_template("premadebox/list.html", boxes=boxes, role=session['role'])