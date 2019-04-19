from flask import Flask,render_template, flash, redirect,url_for
from forms import Register,Login
from flask_sqlalchemy import SQLAlchemy
from models import User, Pitch

app= Flask(__name__) 
app.config['SECRET_KEY']='fe80d26ee9e9e49b181c65aee655938c'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
db = SQLAlchemy(app)


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