from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_user,current_user,logout_user, login_required
from app import db
from . import auth_bp
from ..forms import LoginForm,RegistrationForm
from ..models import User
from flask import render_template

@auth_bp.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        redirect_page = url_for('main.index')
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user=user)
            current_app.logger.info(f"User {current_user.username} logged in")
            next = request.args.get('next')
            if next and next.startswith('/'):
                redirect_page = next
            return redirect(redirect_page)
        else:         
            flash("Incorrect username or password")
    return render_template('auth/login.html',form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    current_app.logger.info(f"User {current_user.username} logging out")    
    logout_user()
    current_app.logger.info(f"User logged out")
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash("Username not available")    
        else:
            user = User(
                username = form.username.data,
                password = form.password.data       
            )
            db.session.add(user)        
            current_app.logger.info(f"Registered {form.username.data}")
            db.session.commit()
            return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)