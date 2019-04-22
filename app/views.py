from flask import render_template, flash, redirect,url_for, request
from app.forms import Register,Login,UpdateAccount
from app.models import User, Pitch
from app import app,db,bcrypt
from flask_login import login_user, current_user, logout_user,login_required


@app.route("/",methods=['GET','POST'])
@app.route("/home",methods=['GET','POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('circles'))
    registerForm = Register()
    if registerForm.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registerForm.password.data).decode('utf-8')
        user = User(username = registerForm.username.data, email = registerForm.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to login!','success')
        return redirect(url_for('home'))
    # else:
    #     flash('Registration Unsuccessful. Details you entered are already taken','danger')
    
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('circles'))
        
        else:
            flash('Login Unsuccessful. Please check email and password','danger')
    #form=form, registerForm=registerForm

    return render_template('home.html', title='login',form=form, registerForm=registerForm )

@app.route("/circle",methods=['GET','POST'])
def circles():
    return render_template('circle.html')

@app.route("/register" ,methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('circles'))
    registerForm = Register()
    if registerForm.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to login!','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', registerForm=registerForm)

@app.route("/login",methods=['GET','POST'])
def login():
    form = Login()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('circles'))
        
        else:
            flash('Login Unsuccessful. Please check email and password','danger')

    return render_template('login.html', title='login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    form = UpdateAccount()
    image_file = url_for('static',filename='images/'+current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file,form=form)
