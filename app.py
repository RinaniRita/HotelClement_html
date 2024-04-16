import mysql.connector, db
from mysql.connector import Error
from markupsafe import escape
from flask import Flask, redirect, url_for, request, render_template, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "RinaniRita"


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

@app.route('/login')
def login():
    return render_template('users/login.html')


@app.route('/register')
def register():
    return render_template('users/register.html')

@app.route('/register', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True).
