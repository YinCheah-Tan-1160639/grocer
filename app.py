from flask import Flask
from database import db
from connect import DB_PASS
from seed import insert_test_data

def register_blueprints(app):
    # Import blueprints and register them
    from routes.store_route import store_bp
    app.register_blueprint(store_bp)


def create_app():

    app = Flask(__name__)

    # Configure database URI
    app.config["SQLALCHEMY_DATABASE_URI"] =\
        f"mysql://root:{DB_PASS}@localhost:3306/fresh_harvest"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    # Bind SQLAlchemy to the app
    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
        insert_test_data()

    # Register blueprints
    register_blueprints(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)