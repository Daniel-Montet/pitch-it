from flask import Blueprint,render_template,flash,url_for,redirect,request
from flask_login import login_user, current_user, logout_user, login_required
from app import db,bcrypt
from app.models import User, Pitch
from app.users.forms import  Register,Login,UpdateAccount, RequestResetForm, ResetPasswordForm
from app.users.utils import save_picture, send_email


users = Blueprint('users',__name__)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account",methods=['GET','POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='images/'+current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file,form=form)


@users.route("/reset_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_email(user)
        flash('An email has been sent with instructions to reset your password.','info')
        return redirect(url_for('main.home'))
    return render_template('reset_request.html', title='Reset Password', form= form)

@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_autheniticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid token','warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registerForm.password.data).decode('utf-8')
        user = User(username = form.username.data, email = registerForm.email.data, password = hashed_password)
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to login!','success')
        return redirect(url_for('main.home'))
    return render_template('reset_token.html', title='Reset Password', form= form)
