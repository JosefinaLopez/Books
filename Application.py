import os 
from flask import Flask, render_template, redirect, session, request, flash
from helps import login_required
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

engine = create_engine(os.getenv("DATABASE_URL"))
# Crea la conexion
db = scoped_session(sessionmaker(bind=engine))


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/', methods=["GET", "POST"])
@login_required
def index():
   # Variables
    busq = request.form.get("Search")
    option = request.form.get("option")

    if request.method == "POST":

        consult = ('%' + busq + '%').title()
        boo = consult.title()
        print(boo)

        if not busq:
            flash("write a search")
            return render_template("index.html")
        else: 
            if option == "Title":
                query = db.execute(text("SELECT Isbn , title, Author, Year From Book WHERE title = :title"), 
                                   {"title":busq})
                row = query.fetchone()
                if row == None:
                     flash("There is no recorded data that matches the given parameter")
                else: 
                    book = row[1]
                    print(book)
                    flash("Successful Search")   
                    return render_template("result.html", busq = row)
            elif option == "Isbn":
                query = db.execute(text("SELECT Isbn , title, Author, Year From Book WHERE isbn = :isbn"), 
                                   {"isbn":busq})
                row = query.fetchone()
            
                print(row)
                if row == None:
                     flash("There is no recorded data that matches the given parameter")
                else: 
                    book = row[1]
                    flash("Successful Search")   
                    return render_template("result.html", busq = busq)
            elif option == "Year":
                query = db.execute(text("SELECT Isbn , title, Author, Year From Book WHERE year = :year"), 
                                   {"year":busq})
                row = query.fetchone()
                print(row)
                if row == None:
                     flash("There is no recorded data that matches the given parameter")
                else:
                    book = row[1]
                    flash("Successful Search")   
                    return render_template("result.html", row = row)
            return render_template("index.html")
    else: 
        return render_template("index.html")

@app.route("/books/<isbn>" ,methods=["GET" ,"POST"])
@login_required
def book(isbn): 

    query = db.execute(text("SELECT *FROM book"))
    return render_template("x")


@app.route('/register', methods=["GET", "POST"])
def register():

    user = request.form.get("Username")
    passw = request.form.get("Password")
    confirm = request.form.get("PasswordConfirm")

    if request.method == "POST":
        if not user:
            flash("Provide a usser")
            return redirect("/register")
        if not passw:
            flash("Provide a Password")
            return redirect("/register")
        if passw != confirm:
            flash("Password do not much")
            return redirect("/register")

        hash = generate_password_hash(passw)
        db.execute(text("INSERT INTO usser (username, password) VALUES(:username, :password)"), 
                   {"username" :user, "password":hash})
        db.commit()
        db.close()
        flash("Successful registration")
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():

    session.clear()
    user = request.form.get("Username")
    passw = request.form.get("Password")

    if request.method == "POST":
        if not user:
            flash("Provide a User")
            return render_template("login.html")
        if not passw:
            flash("Provide a Password")
            return render_template("login.html")

       
        verificar = db.execute(text("SELECT *FROM usser WHERE  username = :username")
                               ,{"username":user})
            
        row = verificar.fetchone()
        print(row[1])
        print(passw)
        print(check_password_hash(row[2], passw))
        if row == None or not check_password_hash(row[2], passw):
            flash("User Or Password Invalid")
            return render_template("login.html")

        session["user_id"] = row[0]
        session["username"] = row[1]
        if row:
            flash("Welcome to Book " + user)
            return redirect("/")
        else:
            flash("User or Password Invalid")
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/lougout")
def lougout():
    session.clear()
    flash("Session Cerrada")
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
