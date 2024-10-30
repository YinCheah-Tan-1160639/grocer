from flask import Blueprint, render_template, abort, request, redirect, session, url_for, flash
from models import Staff, Person, vegetable
from decorators import role_required
from models import Product

staff_bp = Blueprint('staff', __name__, url_prefix='/staff')

@staff_bp.route("/profile")
@role_required('staff')
def profile():
    user = Person.query.get_or_404(session['user_id'])
    return render_template("staff/profile.html", 
                           role=session['role'],
                           username=session['username'],
                           user=user)    

@staff_bp.route("/list_customers")
@role_required('staff')
def list_customers():    
    customers = Staff.list_all_customers()
    return render_template("staff/customer/list.html", 
                        customers=customers, 
                        role=session['role']
                        )

@staff_bp.route("/view_customer/<int:customer_id>")
@role_required('staff')
def view_customer(customer_id):    
    try:        
        customer = Staff.get_customer_details(customer_id)
    except Exception as e:
        flash(str(e), "error")
        return redirect(url_for("staff.list_customers"))
    except Exception as e:
        flash("An unexpected error occurred.", "error")
        return redirect(url_for("staff.list_customers"))
    return render_template("staff/customer/view.html", 
                        customer=customer, 
                        role=session['role']
                        )

@staff_bp.route("/list_veggies")
@role_required('staff')
def list_veggies():   
    veggies = Product().get_all_vegetables()
    return render_template("staff/veggie/list.html", 
                        veggies=veggies, 
                        role=session['role']
                        )

@staff_bp.route("/list_premade_boxes")
@role_required('staff')
def list_premade_boxes():   
    boxes = Product().get_all_premade_boxes()
    return render_template("staff/premadebox/list.html", 
                        boxes=boxes, 
                        role=session['role']
                        )