from flask import Blueprint, render_template, abort, request, redirect, url_for

staff_bp = Blueprint('staff', __name__, url_prefix='/staff')

@staff_bp.route("/list_customers")
def list_customers():    
    return render_template("staff/list_customers.html")