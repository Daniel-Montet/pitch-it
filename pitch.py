from flask import Flask,render_template, flash, redirect,url_for
from forms import Register,Login
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__) 
app.config['SECRET_KEY']='fe80d26ee9e9e49b181c65aee655938c'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Pitch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullabel= False)

    def __repr__(self):
        return f"User('{self.title}','{self.date_posted}')"




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
        flash(f'Account created for {form.username.data} !','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        flash(f'Login successful for {form.username.data} !','success')
        return redirect(url_for('home'))

    return render_template('login.html', title='login', form=form)

 

if __name__ == "__main__":
    app.run(debug=True)