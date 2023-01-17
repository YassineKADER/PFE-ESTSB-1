from flask import Flask, request, render_template, session, redirect, url_for
import pyrebase
import os

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyBgGx67w032_zncuZ37tFYPrm02rH1XbrY",
    "authDomain": "wise-baton-353710.firebaseapp.com",
    "databaseURL": "https://wise-baton-353710-default-rtdb.firebaseio.com",
    "projectId": "wise-baton-353710",
    "storageBucket": "wise-baton-353710.appspot.com",
    "messagingSenderId": "962857669223",
    "appId": "1:962857669223:web:3360987f13c2f1e6787ac2"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
email, password, user = "", "", {}
app.secret_key = os.urandom(28)


@app.route('/')
def index():
    return {'mainview':1}


@app.route('/logout', methods=['POST','GET'])
def logout():
    session.pop('user', None)
    global user
    user = {}
    return redirect('/')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        login_data = request.get_json()
        email = login_data.get("email")
        password = login_data.get("password")
        try:
            global user
            user = auth.sign_in_with_email_and_password(email, password)
            session.pop('user', None)
            session['user'] = user
            return {"login": True}
        except:
            return {"login": False}
    return render_template("Login.html")


@app.route('/forgotpassword', methods=["POST", "GET"])
def forgot():
    if request.method == "POST":
        info = request.get_json()
        email = info.get("email")
        try:
            auth.send_password_reset_email(email)
            return {"sent": True}
        except:
            return {"sent": False}
    return render_template("ForgotPass.html")


@app.route('/dashboard', methods=["POST", "GET"])
def dashboard():
    try:
        if session['user']:
            return render_template("Dashboard.html")
    except:
        return redirect(url_for("login"))
    return redirect(url_for("login"))

@app.route('/user', methods=["POST", "GET"])
def getUser():
    return user;

if __name__ == "__main__":
    app.run(debug=True, port=1212)
