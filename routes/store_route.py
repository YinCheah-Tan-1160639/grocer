from flask import Blueprint, render_template, abort, request, redirect, url_for

store_bp = Blueprint('store', __name__)

@store_bp.route("/")
def index():    
    return render_template("index.html")