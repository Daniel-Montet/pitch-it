from flask import render_template, flash, redirect,url_for
from app.forms import Register,Login
from app.models import User, Pitch
from app import app,db,bcrypt



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/circle")
def circles():
    return render_template('circle.html')

@app.route("/register" ,methods=['GET','POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to login!','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        flash(f'Login successful !','success')
        return redirect(url_for('home'))

    return render_template('login.html', title='login', form=form)
