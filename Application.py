import os
from flask import Flask , render_template, redirect,session,request,flash
from helps import  login_required
from flask_session import Session
from source import conexion
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

con = conexion.conn('localhost', 'postgres','070918','Books')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route ('/')
def index():
  login_required
   #Variables
  busq = request.form.get("Search")
  option = request.form.get("option")

  if request.method == "GET":
      if not busq:
        flash("write a search")
        return render_template("index.html") 
      print("Resultado".format(option)) 
  else:  
    return render_template("index.html")

@app.route ("/search",methods=["GET", "POST"])
def search():
      return render_template("result.html")

@app.route ('/register', methods=["GET", "POST"])
def register():
    
    user = request.form.get("Username")
    passw = request.form.get("Password")
    confirm = request.form.get("PasswordConfirm")
    
    if request.method == "POST":
        if not user:
          flash("Provide a Usser")
          return redirect("/register")
        if not passw:
          flash("Provide a Password")
          return redirect("/register")
        if passw != confirm:
          flash("Password do not much")
          return redirect("/register") 
           
        cursor = con.cursor()  
        hash = generate_password_hash(passw)
        cursor.execute("INSERT INTO Usser (username, password) VALUES(%s, %s)", (user,hash))
        con.commit()
        cursor.close()
        flash("Successful registration")   
        return redirect("/login")
    else:
      return render_template("register.html") 

@app.route ('/login', methods=["GET", "POST"])
def login():
    
    user = request.form.get("Username") 
    passw = request.form.get("Password")

    if request.method == "POST":
        if not user:
            flash("Provide a User")
        if not passw:
           flash("Provide a Password") 

        cursor = con.cursor()
        verificar = cursor.execute("SELECT *FROM Usser WHERE username = %s ", (user,))
        row=cursor.fetchone()
        if row == None or not check_password_hash(row[2],passw):
          flash("User Or Password Invalid")
          return render_template("login.html")  
        
        session["Id"] = row[0]
        session["username"] = row[1]
        if row:
         return redirect("/")
        else: 
          flash("User or Password Invalid")
          return render_template("login.html")
    else:    
     return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True)