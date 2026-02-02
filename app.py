from flask import Flask
from flask import render_template, request, redirect
from werkzeug.security import generate_password_hash
import sqlite3
import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

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
    



@app.route("/login")
def login():
    return render_template("login.html")

