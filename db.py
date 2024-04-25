import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import Error

hostname = 'localhost'
username = 'root'
password1 = 'trung13062005'
databasename = 'hotel-coursework'

def getConnection():
    try:
        conn = mysql.connector.connect(host=hostname,
                                       user = username,
                                       password = password1,
                                       database = databasename)
    except Error as err:
        print(err)
    else:
        if(conn.is_connected):
            return conn
        else:
            conn.close()
            
class Model:
    def __init__(self):
        self.conn = getConnection()
        self.tbName =''
        if self.conn!=None:
            if self.conn.is_connected():
                self.dbcursor = self.conn.cursor()  
        else:
            print('DBfunc error')


    def getAll(self,limit=10):
        try:
            self.dbcursor.execute('select * from '+ self.tbName + ' limit '+ str(limit))
            myresult = self.dbcursor.fetchall()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult

    

class Customer(Model):
    def __init__(self):
       super().__init__()
       self.tbName = 'costumer'
    
    def getById(self, id):
        try:
            self.dbcursor.execute('select * from '+ self.tbName + ' where idcostumer = {}'.format(id))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult
    


    def addNew(self, costumer):
        try:
            self.dbcursor.execute('insert into '+ self.tbName +
                                ' values (%s, %s, %s, %s)',
                                    (costumer['idcostumer'], costumer['cusname'], costumer['email'], costumer['phonenumber']))
            myresult = self.conn.commit()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                return False            
        
        return True
    
    
    def Update(self, costumer):
        try:
            self.dbcursor.execute('update '+ self.tbName +
                                ' set sname = %s, \
                                    email = %s, \
                                    id_cus = %s where idcostumer = %s',
                                    (costumer['cusname'], costumer['email'], costumer['id_cus'], costumer['idcostumer']))
            myresult = self.conn.commit()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                return False            
        
        return True


class Roomstatus(Model):
    def __init__(self):
       super().__init__()
       self.tbName = 'room'
    
    def getById(self, id):
        try:
            self.dbcursor.execute('select * from '+ self.tbName + ' where id_cus ={}'.format(id))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult


class Book(Model):
    def __init__(self):
       super().__init__()
       self.tbName = 'booking'   

    def getById(self, id):
        try:
            self.dbcursor.execute('select * from '+ self.tbName + ' where Room = {}'.format(id))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult

    def addNew(self, book):
        try:
            self.dbcursor.execute('insert into '+ self.tbName + 
                                ' (booking_date, departure_date, adults_number, children_number, roomnumber, users_id) values (%s, %s, %s, %s, %s, %s)',
                                    (book['booking_date'], book['departure_date'], book['adults_number'], book['children_number'], book['roomnumber'], book['users_id']))
            myresult = self.conn.commit()
        except Error as e:
            print(e)
            return False   
        else:    
            if self.dbcursor.rowcount == 0:
                return False      
        return True
    
    
class User(Model):
    def __init__(self):
        super().__init__()
        self.tbName = 'users'
    
    def addNew(self, user):
        try:
            self.dbcursor.execute('insert into '+ self.tbName + 
                                ' (username, email, password_hash, usertype) values (%s, %s, %s, %s)',
                                    (user['username'], user['email'], generate_password_hash(user['password']), user['usertype']))
            myresult = self.conn.commit()
        except Error as e:
            print(e)
            return False   
        else:    
            if self.dbcursor.rowcount == 0:
                return False      
        return True
    
    def getById(self, id):
        try:
            self.dbcursor.execute('select * from '+ self.tbName + ' where id = {}'.format(id))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult
    
    def getByUsername(self, username):
        try: 
            self.dbcursor.execute('select * from '+ self.tbName + ' where username = %s',(username,))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult

    def getByEmail(self, email):
        try:
            self.dbcursor.execute('select * from '+ self.tbName + ' where email = %s',(email,))
            myresult = self.dbcursor.fetchone()
        except Error as e:
            print(e)
            myresult = ()
        else:    
            if self.dbcursor.rowcount == 0:
                myresult = ()            
        
        return myresult 
    
    def checkLogin(self, username, password):
        user = self.getByUsername(username)
        if user=='':
            user = self.getByEmail(username)
        if user:
            # print(user)
            if check_password_hash(user[3], password):
                return True
            
        return False
