from flask import Blueprint

from .documentcontroller import documentcontroller

# Register your blueprints here
controllers_bp = Blueprint('controllers', __name__)

controllers_bp.register_blueprint(documentcontroller)
