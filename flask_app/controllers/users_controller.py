from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def main():
    return render_template("login_register.html")

@app.route('/dashboard')
def dash():
    if not "user_id" in session:
        return redirect('/')
    return render_template("welcome.html")



@app.route('/users/register', methods=['POST'])
def register_user():
    if not User.validator(request.form):
        return redirect('/')
    hashed = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form, 
        'password': hashed
    }
    new_id = User.create(data)
    session['user_id'] = new_id
    return redirect('/dashboard')

@app.route('/users/login', methods=['POST'])
def login_user():
    data = {
        'email' : request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid", "log")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("*Invalid", "log")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/users/logout')
def log_out():
    del session['user_id']
    return redirect('/')