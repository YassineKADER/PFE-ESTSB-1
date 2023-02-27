from flask import Flask, request, render_template, session, redirect, url_for
from run import *
from f_chose_spots import *
import pyrebase
import os, signal
import traceback
import sys
from threading import Thread

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
email, password, user, status = "", "", {}, False
app.secret_key = os.urandom(28)

@app.route('/')
def index():
    try:
        if session['user']:
            return redirect("/login")
    except:
        return redirect("/dashboard")


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
            print(session['user'])
            return render_template("Dashboard.html")
    except:
        return redirect(url_for("login"))
    return redirect(url_for("login"))

@app.route('/user', methods=["POST", "GET"])
def getUser():
    return user;

@app.route('/run', methods=["POST","GET"])
def run():
    if request.method == "POST":
        global status 
        status = True
        data = session['user']
        #print(data["idToken"], data["localId"])
        settings = request.get_json().get("settings")
        url = request.get_json().get("url")
        startfunction = Thread(target=start, args=(settings,data["idToken"], data["localId"],url))
        print(settings, url)
        startfunction.start()
        startfunction.join()
        print("closed")
        sys.exit(startfunction)
    else:
        print("hello")
    return {'status':status}

@app.route('/run/chosespots', methods=["POST", "GET"])
def chosespots():
    if request.method == "POST":
        global status 
        status = True
        url = request.get_json().get("url")
        try:
            start_chosing(videolocation=url)
        except:
            status = False
            return {'status': status}
    else:
        print("hello")
    return {'status':status}


@app.route('/status', methods=["POST", "GET"])
def get_status():
    if request.method == "POST":
        global status
        data = request.get_json()
        status = data.get("status")
    return {"status":status}

@app.route('/signup', methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        sign_up_data = request.get_json()
        email = sign_up_data.get("email")
        password = sign_up_data.get("password")
        try:
            global user
            auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            user_info ={"name": "","location": {"latitude": 0,"longitude": 0, "city":""},"freespace": 0,"totalplace": 0,"maxSizeAtDay": {0:0},"status": False,"description": "","ownername": "","adminname": ""}
            db.child("Users").child(user["localId"]).set(user_info, token=user["idToken"])
        except Exception:
            traceback.print_exc()
            return {"message":"Mail Adress Already Exist"}
        return {"message":"Acount Created"}
    return render_template("signup.html")

@app.route("/signupform", methods=["POST", "GET"])
def forminfo():
    if request.method == "POST":
        name = request.form["name"]
        desc = request.form["description"]
        ownername = request.form["ownername"]
        adminname = request.form["adminname"]
        totalplaces = request.form["totalplace"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        city = request.form["city"]
        print(user)
        db.child("Users").child(user["localId"]).update({"name": name,"location": {"latitude": latitude,"longitude": longitude, "city":city},"status": True,"description": desc,"ownername": ownername,"adminname": adminname}, token=user["idToken"])
        return redirect("/dashboard")
        
    try:
        if session['user']:
            return render_template("signupform.html")
        else:
            return redirect("/")
    except:
        return redirect("/")

@app.route('/quit')
def quit_app():
    os.kill(os.getpid(), signal.SIGINT)
    return { "success": True, "message": "Server is shutting down..." }


if __name__ == "__main__":
    app.run(debug=False, port=1212)
    
