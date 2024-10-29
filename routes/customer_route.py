from flask import Blueprint, render_template, abort, request, redirect, url_for

customer_bp = Blueprint('customer', __name__)

@customer_bp.route("/orders")
def list_orders():    
    return render_template("customer/list_orders.html")