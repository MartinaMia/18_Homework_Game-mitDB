from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User

app = Flask(__name__)

import datetime             # Software importieren
import random

# Controller für index (URL /) mit GET-Methode
@app.route("/", methods=["GET"])
def index():
    current_time = datetime.datetime.now()  # Softwarepaket.Klasse.Methode

    email_address = request.cookies.get("email")       # Cookie-Speicher Mail

    if email_address:                                  # Abgleich mit DB
        user = User.fetch_one(query=["email", "==", email_address])
    else:
        user = None
    return render_template("index.html", user=user, current_time=current_time)

@app.route("/login", methods=["POST"])
def login():
    # name und email aus Eingabefeldern aus index.html erhalten
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    # Secret Number erstellen
    secret_number = random.randint(1, 30)

    # Users Mail mit DB vergleichen
    user = User.fetch_one(query=["email", "==", email]) # Abgleich mit DB

    # Objekt User erstellen und in DB speichern
    if not user:
        user = User(name=name, email=email, secret_number=secret_number)
        user.create()

    # Users Mail in cookie speichern:
    response = make_response(redirect(url_for('index')))    # index.html laden, und zuvor aktualisieren
    response.set_cookie("email", email)             # users mail als cookie speichern

    return response

# Controller für (URL /result) mit POST-Methode
@app.route("/result", methods=["POST"])
def result():
    # Eingabe für guess ermöglichen
    guess = int(request.form.get("guess"))

    email_address = request.cookies.get("email")

    # user mit Hilfe email-Abgleiich erhalten
    user = User.fetch_one(query=["email", "==", email_address])


    if guess == user.secret_number:
        message = "You've guessed it - congratulations! It's number " + str(user.secret_number)

        # wenn gewonnen, neue Nummer erstellen
        new_secret = random.randint(1, 30)

        # update des Users mit erratener Nummer in DB
        User.edit(obj_id=user.id, secret_number=user.secret_number)

    elif guess > user.secret_number:
        message = "Your guess is not correct... try something smaller"


    elif guess < user.secret_number:
        message = "Your guess is not correct... try something bigger"

    return render_template("result.html", message=message)

if __name__ == '__main__':
    app.run(debug=False)

