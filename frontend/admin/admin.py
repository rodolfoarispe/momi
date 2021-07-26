from flask import Blueprint

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin')
def index():
	return "Hello, World! This is the admin page."