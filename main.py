
from flask import Flask,render_template,request,session,redirect,url_for,flash,Response,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import cx_Oracle
conn=cx_Oracle.connect(user="SYSTEM",password="bnm")
local_server=True
app = Flask(__name__)
app.secret_key='lavanya'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI']=cx_Oracle.connect(user="SYSTEM",password="bnm")
#app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/database_table_name'
db=SQLAlchemy(app)
cur= conn.cursor()

def load_user(user_id):
    return User.objects(id=user_id).first()
class User(UserMixin,db.Model):
     fid=db.Column(db.Integer,primary_key=True)
     fname=db.Column(db.String(10))
     email=db.Column(db.String(25))
     password=db.Column(db.String(10))
#sql_create =""""""
class User1(UserMixin,db.Model):
     bid=db.Column(db.Integer,primary_key=True,autoincrement=True)
     bname=db.Column(db.String(10))
     email=db.Column(db.String(15))
     password=db.Column(db.String(1000))
#cur.execute(sql_create)
class addagroproducts(db.Model):
    username=db.Column(db.String(50))
    email=db.Column(db.String(50))
    pid=db.Column(db.Integer,primary_key=True)
    productname=db.Column(db.String(100))
    productdesc=db.Column(db.String(300))
    price=db.Column(db.Integer)
class fdetails(db.Model):
     
    rid=db.Column(db.Integer,primary_key=True)
    fid=db.Column(db.Integer)
    farmername=db.Column(db.String(15))
    adharnumber=db.Column(db.String(20))
    age=db.Column(db.Integer)
    gender=db.Column(db.String(6))
    
    address=db.Column(db.String(50))
    farming=db.Column(db.String(20))
class buyerinfo(db.Model):
     bid=db.Column(db.Integer,primary_key=True)
     name=db.Column(db.String(15))
     email=db.Column(db.String(20))
     mobile=db.Column(db.Integer)
     address=db.Column(db.String(30))


class log(db.Model):
     fid=db.Column(db.Integer,primary_key=True)
class cart(db.Model):
     pid=db.Column(db.Integer,primary_key=True)
     bid=db.Column(db.Integer,primary_key=True,autoincrement=True)
def getlogindetails():
     cur=conn.cursor()
     try:
          loggedIn=True
          loggedIn_buyer=False
          cur.execute("select fid,email from farmeruser where email ={0}").format(session['email'])
          fid,email=cur.fetchone()
          position=0
     except:
           loggedIn=True
           loggedIn_buyer=True
           cur.execute("select bid,email from buser where email ={0}").format(session['email'])
           bid,email=cur.fetchone()
     return(loggedIn,loggedIn_buyer,email,position)

     
def is_valid(email, password):
    con=cx_Oracle.connect(user="SYSTEM",password="bnm")
    
    cur = con.cursor()
    cur.execute('SELECT email, password FROM farmeruser')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == password  :
             
             return True
    return False
def is_valid1(email, password):
    con=cx_Oracle.connect(user="SYSTEM",password="bnm")
    cur = con.cursor()
    cur.execute('SELECT email, password FROM buser')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == password:
            return True
    return False
@app.route("/")
def root():
     
     return render_template('base.html')  
@app.route("/indexf",methods=["POST","GET"])
def login(): 
     if request.method == 'POST':
          if request.form['submit_button']=='Login':
                email=request.form.get('email')
                password=request.form.get('password')
                if is_valid(email, password):
                      session['email']=email
                      return redirect(url_for('farmerhome'))
                else:
                   error = 'Invalid UserId / Password'
                   print("invalid")
                   return render_template('indexf.html', error=error)
          elif request.form['submit_button']=='Sign_up':
               fname=request.form.get('fname')
               email=request.form.get('email')
               password=request.form.get('password')
               execute="""INSERT INTO farmeruser VALUES (:fid,:fname,:email,:password)"""
               cur.execute(execute, {'fid':'','fname':fname, 'email':email, 'password':password})
               conn.commit() 
         

               #return redirect(url_for('indexf'))
            #encpassword=generate_password_hash(password)
     return render_template('indexf.html')
@app.route('/logout')

def logout():
     session.pop('email', None)
     print("Logout SuccessFul","warning")
     return redirect(url_for('login'))
@app.route("/indexb",methods=['POST','GET'])
def login1():
    if request.method == 'POST':
         if request.form['submit_button']=='Login':
              email = request.form['email']
              password = request.form['password']
              if is_valid1(email, password):
                    execute="""INSERT INTO log VALUES (:email)"""
                    cur.execute(execute, {'email':email})
                    conn.commit() 
                    return redirect(url_for('buyerhome'))
              else:
                   error = 'Invalid UserId / Password'
                   print("invalid")
                   return render_template('indexb.html', error=error)
                    
         elif request.form['submit_button']=='Sign_up':
               bname=request.form.get('bname')
               email=request.form.get('email')
               password=request.form.get('password') 
               execute="""INSERT INTO buser VALUES (:bid,:bname,:email,:password)"""
               cur.execute(execute, {'bid':'','bname':bname, 'email':email, 'password':password})
               conn.commit()
               return render_template('indexb.html')
    return render_template('indexb.html')
@app.route('/logout1')
def logout1():
     cur.execute("""delete  from log """)
     conn.commit()
     print("Logout SuccessFul","warning")
     return redirect(url_for('login1'))
@app.route("/dashboard")
def dashboard():
       n_total = cur.var(cx_Oracle.NUMBER)
       cur.callproc('getfcount',[n_total])
       res=n_total.getvalue()
       n_total1 = cur.var(cx_Oracle.NUMBER)
       cur.callproc('getcustomercount',[n_total1])
       res1=n_total1.getvalue()
       n_total2 = cur.var(cx_Oracle.NUMBER)
       cur.callproc('getocount',[n_total2])
       res4=n_total2.getvalue()
       n_total3 = cur.var(cx_Oracle.NUMBER)
       cur.callproc('gettotal',[n_total3])
       res5=n_total3.getvalue()

       cur.execute("select name,mobile,address from buyerinfo")
       res2=cur.fetchall()
       cur.execute("select rid,fid,farmername,adharnumber,age,gender,farming from fdetails ")
       res3=cur.fetchall()
   
       return render_template('dashboard.html',res=res,res1=res1,res2=res2,res3=res3,res4=res4,res5=res5)
@app.route("/farmerregister",methods=['POST','GET'])

def farmerregister():
     conn=cx_Oracle.connect(user="SYSTEM",password="bnm")
     cur= conn.cursor()
     if request.method == "POST":     
            fid=request.form.get('fid')
            farmername=request.form.get('farmername')
            adharnumber=request.form.get('adharnumber')
            age=request.form.get('age')
            gender=request.form.get('gender')
            address=request.form.get('address')
            farming=request.form.get('farming')
            execute="""INSERT INTO fdetails VALUES (:rid,:farmername,:fid,:adharnumber,:age,:gender,:address,:farming)"""
            #execute="""INSERT INTO Addagroproduct VALUES (:username,:email,:pid,:productname,:productdesc,:price)"""
            cur.execute(execute, {'rid':'','farmername':farmername,'fid':fid,'adharnumber' :adharnumber, 'age':age,'gender':gender, 'address':address,'farming':farming })
            conn.commit()
     return render_template('farmerregister.html')
@app.route("/fview",methods=['POST','GET'])
def viewfarmer():
     conn=cx_Oracle.connect(user="SYSTEM",password="bnm")
     cur= conn.cursor()
     cur.execute("SELECT * FROM fdetails,farmeruser f where f.email='{0}'".format(session['email']))
     res=cur.fetchall()
     return render_template('fview.html',res=res)
@app.route("/navbar")
def navbar():
     return render_template('navbar.html')
@app.route("/farmerhome")
def farmerhome():
       return render_template('farmerhome.html')
@app.route("/buyerhome")
def buyerhome():
     return render_template('buyerhome.html') 
@app.route("/bhome")
def bhome():
     return render_template('bhome.html') 
@app.route("/buyerinfo",methods=['POST','GET'])
def buyerinfo1():
      if request.method == "POST":
        name=request.form.get('name')
        bid=request.form.get('bid')
        email=request.form.get('email')
        mobile=request.form.get('mobile')
        address=request.form.get('address')
        execute="""INSERT INTO buyerinfo VALUES (:bid,:name,:email,:mobile,:address)"""
        cur.execute(execute, {'bid':bid,'name':name,'email' :email, 'mobile':mobile,'address':address })
        conn.commit()
      return render_template('buyerinfo.html')

@app.route("/update",methods=['POST','GET'])
def update():
     
      conn=cx_Oracle.connect(user="SYSTEM",password="bnm")
      cur = conn.cursor()
      if request.method == "POST":
        
          fname=request.form.get('fname')
          email=request.form.get('email')
          password=request.form.get('password')
          cur.execute("UPDATE farmeruser SET fname='{0}',email='{1}',password='{2}' where email='{3}'".format(fname,email,password,session['email']))
          
          conn.commit()
      return render_template('update.html')
@app.route("/delete",methods=['POST','GET'])
def delete():
      conn=cx_Oracle.connect(user="SYSTEM",password="bnm")
      cur = conn.cursor()
      
      cur.execute("select * from farmeruser where email='{0}'".format(session['email']))
      fid=cur.fetchone()[0] 
      print(fid)
      print("hi")
      execute="DELETE from farmeruser where fid='{0}'".format(fid)
      cur.execute(execute)
      print("lol")
      conn.commit()
      print("user deleted")
      return render_template('farmerhome.html')

@app.route("/cart",methods=['POST'])
def addtocart():
      pid = request.form['pid']
      
      conn=cx_Oracle.connect(user="SYSTEM",password="bnm")
      cur = conn.cursor()
      if request.method == "POST":
        cur.execute("select email from log")
        email = cur.fetchone()[0] 
        cur.execute("SELECT bid FROM buser WHERE email ='{0}'".format(email))
        bid = cur.fetchone()[0] 
        execute=("INSERT INTO cart VALUES (:cid,:bid,:pid,:quantity)")
        cur.execute(execute,{'cid':'','bid':bid,'pid':pid,'quantity':1})
        conn.commit()
        print("Added successfully")
        
      return render_template('buyerhome.html')
@app.route("/cart1")
def cart1():
     conn=cx_Oracle.connect(user="SYSTEM",password="bnm")
     cur = conn.cursor()
     cur.execute("select b.bid from log l , buser b where l.email=b.email")
     bid= cur.fetchone()[0] 
     cur.execute("SELECT p.productname,p.price, b.bname FROM cart c, addagroproducts p,buser b where c.pid=p.pid and b.bid=c.bid and b.bid='{0}'".format(bid))
     res=cur.fetchall() 
     
     t=0
     for a in res:
          t+=a[1]
     print(t)
     return render_template('cart1.html',res1=res,t=t)
@app.route("/order",methods=['POST'])
def order():
       conn=cx_Oracle.connect(user="SYSTEM",password="bnm")
       cur = conn.cursor()
       
       productname = request.form['productname']
       if request.method == "POST":
        cur.execute("select email from log")
        email = cur.fetchone()[0] 
        cur.execute("SELECT bname FROM buser WHERE email ='{0}'".format(email))
        bname = cur.fetchone()[0] 
        cur.execute("select fid from addagroproducts where productname='{0}'".format(productname))
        fid=cur.fetchone()[0]
        execute=("INSERT INTO orderitem VALUES (:foid,:fid,:bname,:pname)")
        cur.execute(execute,{'foid':'','fid':fid,'bname':bname,'pname':productname})
        conn.commit()
        print("Added successfully")
       
     


        
       return render_template('buyerhome.html')

@app.route('/agroproducts',methods=['POST','GET'])
def agroproducts():
      conn=cx_Oracle.connect(user="SYSTEM",password="bnm")
      cur= conn.cursor()
      cur.execute("""SELECT * FROM addagroproducts""") 
      res=cur.fetchall()
      return render_template('agroproducts.html',res1=res)

@app.route('/addagroproducts',methods=['POST','GET'])
def addagroproducts1():
     conn=cx_Oracle.connect(user="SYSTEM",password="bnm")
     cur= conn.cursor()
     if request.method == "POST":
            username=request.form.get('username')
            email=request.form.get('email')
            pid=request.form.get('pid')
            productname=request.form.get('productname')
            productdesc=request.form.get('productdesc')
            price=request.form.get('price')
            fid=request.form.get('fid')
            execute="""INSERT INTO addagroproducts VALUES (:username,:email,:pid,:productname,:productdesc,:price,:fid)"""   
            #execute="""INSERT INTO Addagroproduct VALUES (:username,:email,:pid,:productname,:productdesc,:price)"""
            cur.execute(execute, {'username':username, 'email':email, 'pid':pid, 'productname' :productname, 'productdesc' :productdesc, 'price':price,'fid':fid})
            conn.commit()
   
     return render_template('addagroproducts.html')
@app.route('/agro')

def agro():
      conn=cx_Oracle.connect(user="SYSTEM",password="bnm")
      cur= conn.cursor()
      cur.execute("""SELECT * FROM addagroproducts""") 
      res=cur.fetchall()
     
      return render_template('agro.html',res1=res)
@app.route('/card')

def card():
    
      return render_template('card.html')
@app.route('/transaction')

def transaction():
    
      return render_template('transaction.html')
@app.route('/message')

def message():
    
      return render_template('message.html')


@app.route('/vieworders')

def view():
      conn=cx_Oracle.connect(user="SYSTEM",password="bnm")
      cur= conn.cursor()
      cur.execute("select fid from farmeruser where email ='{0}'".format(session['email']))
      fid = cur.fetchone()[0] 
      print(fid)
     
      cur.execute("SELECT f.bname,f.pname  FROM orderitem f  where f.fid='{0}'".format(fid)) 
      res=cur.fetchall()
     
    
      return render_template('vieworders.html',res=res)
     


     


app.run(debug=True)
