import secrets
import os
from flask import render_template, flash, redirect,url_for, request, abort
from app.forms import( Register,Login,UpdateAccount,
         PostForm, CommentForm, RequestResetForm, ResetPasswordForm)
from app.models import User, Pitch, Comment
from app import app,db,bcrypt
from flask_login import login_user, current_user, logout_user,login_required
from flask_mail import Message
from .email import mail_message


@app.route("/",methods=['GET','POST'])
@app.route("/home",methods=['GET','POST'])
def home():
    posts = Pitch.query.all()
    comments = Comment.query.all()
    
    # if current_user.is_authenticated:
    #     return redirect(url_for('circles'))
    registerForm = Register()
    if registerForm.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registerForm.password.data).decode('utf-8')
        user = User(username = registerForm.username.data, email = registerForm.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to login!','success')
        mail_message("Welcome to watchlist","email/welcome_user",user.email,user=user)
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

    return render_template('home.html', title='login',form=form, registerForm=registerForm ,posts=posts, comments=comments)

@app.route("/circle",methods=['GET','POST'])
def circles():
    return render_template('circle.html')

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
    form = PostForm()
    if form.validate_on_submit():
        flash('Your post has been created!','success')
        hashtag=''
        hashtags= form.content.data
        print(hashtags)
        newstr= hashtags.split()
        for char in newstr:
            if char.startswith("#"):
                hashtag=char.strip("#")
                print(hashtag)
                post = Pitch(title = form.title.data, content= form.content.data, author = current_user,hashtags=hashtag)
                db.session.add(post)
                db.session.commit()
                return redirect(url_for('home'))
        
    return render_template('create_post.html', title='New Post',form=form,legend='New Post') 

@app.route("/post/<int:post_id>",methods=['GET','POST'])
def post(post_id):
    review= CommentForm()
    comments = Comment.query.all()
    post = Pitch.query.get_or_404(post_id)
    if review.validate_on_submit():
        comment = Comment(body= review.comment.data,post_id=post.id )
        db.session.add(comment)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('post',post_id=post.id))
    return render_template('post.html',title = post.title, post=post,review=review, comments = comments )

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Pitch.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    # form.title.data = post.title
    # form.content.data = post.content
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Updated Post')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
    form=form,legend='Update Post')

@app.route("/post/<int:post_id>/delete",methods=['GET','POST'])
def delete_post(post_id):
    post = Pitch.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('home'))


def send_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                sender='noreply@demo.com',
                recipients=[user.email])
    msg.body = '''To reset your password, visit the following link:
{url_for('reset_token', token = token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made
'''



@app.route("/reset_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_email(user)
        flash('An email has been sent with instructions to reset your password.','info')
        return redirect(url_for('home'))
    return render_template('reset_request.html', title='Reset Password', form= form)

@app.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_autheniticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid token','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registerForm.password.data).decode('utf-8')
        user = User(username = form.username.data, email = registerForm.email.data, password = hashed_password)
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to login!','success')
        return redirect(url_for('home'))
    return render_template('reset_token.html', title='Reset Password', form= form)
