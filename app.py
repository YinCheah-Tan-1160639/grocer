from flask import Flask
from database import db
from hashing import hashing
from sqlalchemy import create_engine
from connect import DB_USER, DB_PASS, DB_NAME, DB_HOST, DB_PORT
from seed import insert_test_data

def register_blueprints(app):
    # Import blueprints and register them
    from routes import store_bp, staff_bp, customer_bp
    app.register_blueprint(store_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(customer_bp)

    # from routes.store_route import store_bp
    # app.register_blueprint(store_bp)


def create_app():

    app = Flask(__name__)

    app.secret_key = 'mpXQwobkD5'

    # Configure database URI
    app.config["SQLALCHEMY_DATABASE_URI"] =\
        f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'max_identifier_length' : 64}
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    # Bind SQLAlchemy to the app
    db.init_app(app)

    hashing.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
        insert_test_data()

    # Register blueprints
    register_blueprints(app)

    return app

# For WSGI
app = create_app() 

if __name__ == '__main__':
    # app = create_app()
    app.run(debug=True)

