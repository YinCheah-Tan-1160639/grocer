from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from decorators import role_required
from models import Customer
from models import Staff
from models import PremadeBoxProduct
from models import VegetableProduct
from models import Order
from models import CorporateCustomer
from models import db

staff_bp = Blueprint('staff', __name__, url_prefix='/staff')

@staff_bp.route("/profile")
@role_required("staff")
def profile():
    user = Staff.query.get_or_404(session['user_id'])
    return render_template("staff/profile.html", 
                           role=session['role'],
                           username = session['username'],
                           user=user)    

@staff_bp.route("/list_customers")
@role_required("staff")
def list_customers():    
    customers = Customer.query.all()  
    if not customers:
        flash("No customers found.", "warning")
    return render_template("staff/customer/list.html", 
                        customers=customers, 
                        role=session['role']
                        )

@staff_bp.route("/view_customer/<int:customer_id>")
@role_required("staff")
def view_customer(customer_id):        
    customer = Customer.query.get_or_404(customer_id)
    return render_template("staff/customer/view.html", 
                        customer=customer, 
                        role=session['role']
                        )

@staff_bp.route("/list_veggies")
@role_required("staff")
def list_veggies():  
    available = request.args.get("available", None)
    if available is not None and available in ["0", "1"]: 
        if available == "1":
            available = True
        elif available == "0":
            available = False
        veggies = VegetableProduct.query.filter_by(available=available).all()
        if not veggies:
            flash("No vegetables found.", "warning")
    else:
        veggies = VegetableProduct.query.order_by(VegetableProduct.name).all()
        if not veggies:
            flash("No vegetables found.", "warning")

    return render_template("veggie/list.html", veggies=veggies, role=session['role'])

size_order = {
    'small': 1,
    'medium': 2,
    'large': 3
}

@staff_bp.route("/list_premade_boxes")
@role_required("staff")
def list_premade_boxes():    
    boxes = PremadeBoxProduct.query.all()
    if not boxes:
        flash("No premade boxes found.", "warning")
    sorted_boxes = sorted(boxes, key=lambda box: size_order.get(box.size, 4))
    return render_template("premadebox/list.html", 
                        boxes=sorted_boxes, 
                        role=session['role'])


@staff_bp.route("/list_orders")
@role_required("staff")
def list_orders():
    """This route allows the staff to view a list of orders."""    
    orders = Order.query.filter(Order.status != "Pending").order_by(Order.date.desc()).all()
    if not orders:
        flash("No orders found.", "error")
    return render_template("customer/order/list.html", orders=orders, role=session['role'])  

@staff_bp.route("/order/<int:order_id>/view")
@role_required("staff")
def view_order(order_id): 
    """This route allows the staff to view an order."""   
    order = Order.query.get_or_404(order_id)
    if not order:
        flash("Order not found.", "error")
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

@staff_bp.route("/<int:order_id>/update", methods=["POST"])
@role_required("staff")
def update_order(order_id): 
    """This route allows the staff to update the status of an order."""   
    order = Order.query.get_or_404(order_id)
    if not order:
        flash("Order not found.", "error")
        return redirect(url_for('staff.list_orders'))
    if request.form.get("status"):
        status = request.form.get("status")
        try:
            order.update_status(status)
            db.session.commit()
            flash("Order status updated.", "success")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for('staff.view_order', order_id=order_id))
    flash("Invalid status.", "error")
    return redirect(url_for('staff.list_orders'))