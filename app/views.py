import secrets
import os
from flask import render_template, flash, redirect,url_for, request, abort
from app.forms import( Register,Login,UpdateAccount,
         PostForm, CommentForm, RequestResetForm, ResetPasswordForm)
from app.models import User, Pitch, Comment
from app import app,db,bcrypt
from flask_login import login_user, current_user, logout_user,login_required
from flask_mail ifrom flask_mail import Message
from .email import mail_messagemport Message
from .email import mail_message


