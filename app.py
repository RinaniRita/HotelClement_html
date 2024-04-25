import mysql.connector, db
from mysql.connector import Error
from markupsafe import escape
from flask import Flask, redirect, url_for, request, render_template, session, jsonify
from functools import wraps

app = Flask(__name__)
app.secret_key = "RinaniRita"


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_login' in session:
            return f(*args, **kwargs)
        else:            
            print("You need to login first")
            return render_template('users/login.html', error='You need to login first')    
    return wrap

@app.route('/account')
@login_required
def account():
    username=''
    if 'username' in session and 'is_login' in session and session['is_login']:
        username = session['username']
    return render_template('account.html',  username = username)

@app.route('/')
def home():
    username=''
    if 'username' in session and 'is_login' in session and session['is_login']:
        username = session['username']
    return render_template('Home.html',  username = username)

@app.route('/Book',  methods=['GET', 'POST'])
@login_required
def book():
    if request.method == 'POST':
        usermodel = db.Book()
        book = dict()
        book['booking_date']= request.form['booking_date']
        book['departure_date']=request.form['departure_date']
        book['adults_number']=request.form['adults_number']
        book['children_number']=request.form['children_number']
        book['roomnumber']=request.form['roomnumber']
        book['users_id'] = session['id']
        print(book)
        if usermodel.addNew(book):
            return redirect(url_for('home'))   
    
    username = session['username'] if 'username' in session and session['username']!='' else ''
    return render_template('Book.html', username = username)

@app.route('/contact_us')
def contact_us():
    username = session['username'] if 'username' in session and session['username']!='' else ''
    return render_template('contact_us.html', username = username)

@app.route('/Gallery')
def gallery():
    username = session['username'] if 'username' in session and session['username']!='' else ''
    return render_template('Gallery.html',username = username)

@app.route('/Online_booking')
def online_booking():
    username = session['username'] if 'username' in session and session['username']!='' else ''
    return render_template('Online_booking.html', username = username)

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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and request.form['username']!='':
        username = request.form['username']
        password = request.form['password']
        usermodel = db.User() 
        if usermodel.checkLogin(username, password):
                session['username'] = username
                user = usermodel.getByUsername(username)
                session['id'] = user[0]
                session['is_login'] = True
                return redirect(url_for('home')) 
        else:
            error_message = 'Username not found or Invalid password'
            return render_template('users/login.html', error=error_message)
    return render_template('users/login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        usermodel = db.User()
        user = dict()
        user['username']= request.form['username'].strip()
        if (user['username'] =='') or (user['username'] == usermodel.getByUsername(user['username'])):
            error_message = 'existed username'
            return render_template('users/register.html', error = error_message)

        user['email'] = request.form['email']
        if user['email']=='' or usermodel.getByEmail(user['email']):
            error_message = 'existed email'
            return render_template('users/register.html', error = error_message)

        if request.form['password']!='' and request.form['password']==request.form['repassword']:
            user['password'] = request.form['password']
        else:
            user['password']=''
        user['usertype'] = ''
        if user['password']!='':
            usermodel = db.User()
            if usermodel.addNew(user):
                return redirect(url_for('login'))   
    return render_template('users/register.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    session.pop('is_login', None)
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
