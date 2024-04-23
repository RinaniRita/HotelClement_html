import mysql.connector, db
from mysql.connector import Error
from markupsafe import escape
from flask import Flask, redirect, url_for, request, render_template, session
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "RinaniRita"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_username(self, field):
        existing_user = User.query.filter_by(username=field.data).first()
        if existing_user:
            raise ValidationError('That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/Book')
def book():
    return render_template('Book.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/Gallery')
def gallery():
    return render_template('Gallery.html')

@app.route('/Online_booking')
def online_booking():
    return render_template('Online_booking.html')

@app.route('/Terms_of_service')
def Terms_of_service():
    return render_template('Terms_of_service.html')

@app.route('/payments')
def payments():
    return render_template('payments_info.html')

@app.route('/admin')
def admin():
    return render_template('admin/admin.html')

@app.route('/booking')
def booking():
    return render_template('admin/booking.html')

@app.route('/customers')
def customers():
    return render_template('admin/customers.html')

@app.route('/earnings')
def earnings():
    return render_template('admin/earnings.html')

@app.route('/profile')
def profile():
    return render_template('admin/profile.html')

@app.route('/reports')
def reports():
    return render_template('admin/reports.html')

@app.route('/rooms')
def rooms():
    return render_template('admin/rooms.html')

@app.route('/setting')
def setting():
    return render_template('admin/setting.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect('/dashboard')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Retrieve the user from the database
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Authentication successful
            session['user_id'] = user.id
            return redirect('/dashboard')
        else:
            # Authentication failed
            error = 'Invalid username or password'
            return render_template('users/login.html', form=form, error=error)

    return render_template('users/login.html', form=form)

@app.route('/register')
def register():
    if request.method == 'POST':
        user = dict()
        # username = request.form['username']
        # password = request.form['password']
        user['username']= request.form['username']
        user['password'] = request.form['password']
        user['email'] = request.form['email']
        uniqueFlag = True
        usermodel = db.User()
        usermodel.addNew(user)
        user['username']= request.form['username']
        if user['username']=='' or usermodel.getByUsername(user['username']):
            uniqueFlag = False
        
        user['email'] = request.form['email']
        if user['email']=='' or usermodel.getByEmail(user['email']):
            uniqueFlag = False

        if request.form['password']!='' and request.form['password']==request.form['repassword']:
            user['password'] = request.form['password']
        else:
            user['password']=''
        user['usertype'] = ''
        if uniqueFlag and  user['password']!='':
            usermodel = db.User()
            return user['password']
        if usermodel.addNew(user):
            return redirect(url_for('index'))        
    return render_template('users/register.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
