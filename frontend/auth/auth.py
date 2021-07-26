from flask import Blueprint, render_template, request, redirect, flash, url_for
from ..forms import RegistrationForm

from .. import db
from ..models import User

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@auth_bp.route('/logout')
def logout():
    return 'Logout'