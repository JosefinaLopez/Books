import os
from flask import Flask, render_template, redirect, session, request, flash
from helps import login_required
from flask_session import Session
from source import conexion
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import requests
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

PGHOST = os.environ.get('PGHOST')
PGUSER = os.environ.get('PGUSER')
PGPASSWORD = os.environ.get('PGPASSWORD')
PGDATABASE = os.environ.get('PGDATABASE')

print(PGHOST, PGUSER, PGPASSWORD, PGDATABASE)

con = conexion.conn(PGHOST, PGUSER, PGPASSWORD, PGDATABASE)

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
        if not busq:
            flash("write a search")
            return render_template("index.html")
        else:
            cursor = con.cursor()
            if option == "Title":
                cursor.execute(
                    "SELECT isbn , title, author,year FROM books WHERE title = %s", (busq,))
                row = cursor.fetchone()
            elif option == "Isbn":
                cursor.execute("SELECT *FROM books WHERE Isbn = %s", (busq,))
                row = cursor.fetchone()
            elif option == "Year":
                cursor.execute("SELECT *FROM books WHERE year = %s", (busq,))
                row = cursor.fetchone()
            print(row)
            return render_template("index.html")
    else:
        return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template("result.html")

@app.route('/data')
def datos():
    isbn = request.args.get("isbn")
    # 0743454553
    data = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:0380795272").json()
    
    return data

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

        cursor = con.cursor()
        hash = generate_password_hash(passw)
        cursor.execute(
            "INSERT INTO usser (username, password) VALUES(%s, %s)", (user, hash))
        con.commit()
        cursor.close()
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

        cursor = con.cursor()
        verificar = cursor.execute(
            "SELECT *FROM usser WHERE username = %s ", (user,))
        row = cursor.fetchone()
        print(row[2])
        print(passw)
        print(check_password_hash(row[2], passw))
        if row == None or not check_password_hash(row[2], passw):
            flash("User Or Password Invalid")
            return render_template("login.html")

        session["user_id"] = row[0]
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
