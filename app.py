import mysql.connector, db
from mysql.connector import Error
from markupsafe import escape
from flask import Flask, redirect, url_for, request, render_template, session
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

@app.route('/')
def home():
    username=''
    if 'username' in session and 'is_login' in session and session['is_login']:
        username = session['username']
    return render_template('Home.html',  username = username)

@app.route('/Book')
def book():
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
    username = session['username'] if 'username' in session and session['username']!='' else ''
    return render_template('Terms_of_service.html', username = username)

@app.route('/admin')
def admin():
    username = session['username'] if 'username' in session and session['username']!='' else ''
    return render_template('admin.html', username = username)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and request.form['username']!='':
        username = request.form['username']
        password = request.form['password']
        usermodel = db.User()
        if usermodel.checkLogin(username, password):
            session['username'] = username
            session['is_login'] = True
            return redirect(url_for('home'))
        
    return render_template('users/login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        uniqueFlag = True
        usermodel = db.User()
        user = dict()
        user['username']= request.form['username']
        user['password'] = request.form['password']
        user['email'] = request.form['email']
        if (user['username'] =='' and user['username'] != ['trung', 'nhatminh1', 'nhatminh2'] )  or usermodel.getByUsername(user['username'])  :
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
            if usermodel.addNew(user):
                return redirect(url_for('login'))        
    return render_template('users/register.html')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
