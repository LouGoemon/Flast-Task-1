from config import app,db,bcrypt, User
from flask import Flask, render_template,redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required

import forms

@app.route('/',methods = ['GET','POST'])
@app.route('/index',methods = ['GET','POST'])

def hello_world():
    if forms.RegistrationForm().validate_on_submit():
        register_form = forms.RegistrationForm()       
        hashed_password =   bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
        user = User(username = register_form.username.data,
                    email = register_form.email.data,
                    password = hashed_password)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(
               email = forms.RegistrationForm().email.data).first()
       
        if user and bcrypt.check_password_hash(
        user.password, forms.RegistrationForm().password.data):
           
           login_user(user)

        if (request.method == "POST") & (request.form.get('post_header') == 'log out'):

            logout_user()
            return redirect(url_for('hello_world'))
    if forms.LoginForm().validate_on_submit():
    
        login_form = forms.LoginForm()
        user = User.query.filter_by(email =  
               login_form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
                login_user(user, remember = login_form.remember.data)
                return redirect(url_for('hello_world'))

    return render_template('index.html',
                           login_form = forms.LoginForm(),
                           register_form = forms.RegistrationForm())