from .store_route import store_bp
from .staff_route import staff_bp
from .customer_route import customer_bp

# Expose all blueprints so they can be imported from routes
__all__ = ["store_bp", "staff_bp", "customer_bp"]