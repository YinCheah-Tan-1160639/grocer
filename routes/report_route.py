from tracemalloc import start
from turtle import st
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from datetime import datetime, timedelta
from decorators import role_required
from sqlalchemy import func
from models import db, Order, OrderLine, Item

report_bp = Blueprint('report', __name__, url_prefix='/report')

def generate_sales_report(start_date: datetime, end_date: datetime) -> dict:
    
    orderlines = (
        db.session.query(OrderLine)
        .join(OrderLine.order)
        .filter(
            Order.date >= start_date,
            Order.date <= end_date,
            Order.status.in_(['Completed', 'Confirmed', 'Ready for Pickup', 'Shipped'])
        )
        .all()
    )

    total_sales = sum(orderline.item.calculate_subtotal() for orderline in orderlines if orderline.item is not None)

    return total_sales

def get_order_count(start_date, end_date):
    return (
        db.session.query(Order)
        .filter(
            Order.date >= start_date, 
            Order.date <= end_date, 
            Order.status.in_(['Confirmed', 'Ready for Pickup', 'Shipped', 'Completed'])
        )
        .count()
    )

def get_delivery_order(start_date, end_date):
    return (
        db.session.query(Order)
        .filter(
            Order.date >= start_date, 
            Order.date <= end_date, 
            Order.is_delivery == True,
            Order.status.in_(['Confirmed', 'Shipped', 'Completed'])
        )
        .count()
    )

def get_pickup_order(start_date, end_date):
    return (
        db.session.query(Order)
        .filter(
            Order.date >= start_date, 
            Order.date <= end_date, 
            Order.is_delivery == False,
            Order.status.in_(['Confirmed', 'Ready for Pickup', 'Completed'])
        )
        .count()
    )

def get_most_popular_item(start_date: datetime, end_date: datetime):
    most_popular_item = (
        db.session.query(
            Item.name,
            func.sum(OrderLine.quantity).label('total_quantity')
        )
        .join(OrderLine)
        .join(Order)
        .filter(
            Order.date >= start_date,
            Order.date <= end_date,
            Order.status.in_(['Completed', 'Confirmed', 'Ready for Pickup', 'Shipped'])
        )
        .group_by(Item.id)
        .order_by(func.sum(OrderLine.quantity).desc())
        .first()
    )
    return most_popular_item

def get_most_popular_item(start_date: datetime, end_date: datetime):
    # Query all OrderLines within the date range
    orderlines = (
        db.session.query(OrderLine)
        .join(Order)
        .filter(
            Order.date >= start_date,
            Order.date <= end_date,
            Order.status.in_(['Completed', 'Confirmed', 'Ready for Pickup', 'Shipped'])
        )
        .all()
    )

    # Calculate total quantities for each item
    item_totals = {}
    for orderline in orderlines:
        item_name = orderline.item.name if hasattr(orderline.item, 'name') else orderline.item.box_name()
        quantity = orderline.item.get_quantity()

        if item_name in item_totals:
            item_totals[item_name] += quantity
        else:
            item_totals[item_name] = quantity

    # Find the most popular item based on total quantity sold
    if item_totals:
        most_popular_item = max(item_totals, key=item_totals.get)
        total_quantity = item_totals[most_popular_item]
        return {"name": most_popular_item, "total_quantity": total_quantity}
    else:
        return None

@report_bp.route("/report", methods=['GET', 'POST'])
@role_required("staff")
def sales_report(): 
    """This route allows the staff to view and generate sales report."""
    report_types = ['Weekly', 'Monthly', 'Yearly']
    if request.method == 'GET':         
        return render_template('staff/report.html', 
                            report_types=report_types,
                            role=session['role'],                            
                           )  

    else:
        type = request.form.get('report_type')  # Get report type from form

        # Get start and end dates based on the report type
        if type == 'Weekly':
            end_date = datetime.today()
            start_date = end_date - timedelta(days=6)
        elif type == 'Monthly':
            end_date = datetime.today()
            start_date = end_date.replace(day=1)  # First day of the current month
        elif type == 'Yearly':
            end_date = datetime.today()
            start_date = end_date.replace(month=1, day=1)  # First day of the year
        else:
            flash("Invalid report type", "error")
            return redirect(url_for('report.sales_report'))

        # Fetch report data
        total_sales = generate_sales_report(start_date, end_date)
        order_count = get_order_count(start_date, end_date)
        delivery_order = get_delivery_order(start_date, end_date)
        pickup_order = get_pickup_order(start_date, end_date)

        start_date = start_date.strftime('%d-%B-%Y')
        end_date = end_date.strftime('%d-%B-%Y')

        return render_template('staff/report.html', 
                            start_date=start_date,
                            end_date=end_date,
                            total_sales=total_sales, 
                            order_count=order_count,
                            delivery_order=delivery_order,
                            pickup_order=pickup_order, 
                            type=type,
                            role=session['role'],
                            report_types=report_types
                            )

@report_bp.route("/most_popular_item", methods=['GET', 'POST'])
@role_required("staff")
def most_popular_item(): 
    """This route allows the staff to view the most popular item."""   
    
    today = datetime.today().strftime('%Y-%m-%d')
    
    if request.method == 'GET':
        return render_template('staff/popular_item.html', 
                            max_date=today,                           
                            role=session['role'],
                            )
    else:
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if start_date == '' or end_date == '':
            flash("Please select a date range", "error")
            return redirect(url_for('report.most_popular_item'))
        
        try:
            # Parse the date strings into datetime objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            # Check if the end date is later than the start date
            if end_date <= start_date:
                flash("End date must be later than start date", "error")
                return redirect(url_for('report.most_popular_item'))
            
        except ValueError:
            flash("Invalid date format", "error")
            return redirect(url_for('report.most_popular_item'))

        item = get_most_popular_item(start_date, end_date) 

        start_date = start_date.strftime('%d-%B-%Y')    
        end_date = end_date.strftime('%d-%B-%Y')
        return render_template('staff/popular_item.html', 
                            start_date=start_date,
                            end_date=end_date,
                            item=item, 
                            max_date=today,                           
                            role=session['role'],
                            )