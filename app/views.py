import secrets
import os
from flask import render_template, flash, redirect,url_for, request
from app.forms import Register,Login,UpdateAccount, PitchForm
from app.models import User, Pitch
from app import app,db,bcrypt
from flask_login import login_user, current_user, logout_user,login_required


@app.route("/",methods=['GET','POST'])
@app.route("/home",methods=['GET','POST'])
def home():
    posts = Pitch.query.all()
    # if current_user.is_authenticated:
    #     return redirect(url_for('circles'))
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

    return render_template('home.html', title='login',form=form, registerForm=registerForm ,posts=posts)

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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images',picture_fn)
    form_picture.save(picture_path)
    return picture_fn



@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file= picture_file
            
        current_user.username= form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='images/'+current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file,form=form)

@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form = PitchForm()
    if form.validate_on_submit():
        flash('Your post has been created!','success')
        pitch = Pitch(title = form.title.data, content= form.content.data, author = current_user)
        db.session.add(pitch)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',form=form) 

@app.route("/post/<int:post_id>",methods=['GET','POST'])
def post(post_id):
    post = Pitch.query.get_or_404(post_id)
    return render_template('post.html',title = post.title, post=post)