from flask import Flask
from flask import session
from flask import render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/loginPost)", methods=["POST"])
def loginPost():

    username = request.form["username"]
    password = request.form["password1"]
    
    sql = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(sql, [username])[0][0]
    if check_password_hash(password_hash, password):
        session["username"] = username
        return render_template("Homepage.html", message="Kirjautuminen onnistui.")
    else:
        return render_template("loginPost.html", message="Väärä käyttäjätunnus tai salasana.")
    
    
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registered",methods=["POST"])
def registered():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("registered.html",message="Salasanat eivät täsmää.")
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return  render_template("registered.html",message="Käyttäjätunnus on jo olemassa.")
    return render_template("registered.html",message="Käyttäjätunnus luotu onnistuneesti.")
    




