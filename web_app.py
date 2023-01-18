from flask import Flask, request, render_template, session, redirect, url_for
from run import *
from f_chose_spots import *
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
        start(False,user_token="eyJhbGciOiJSUzI1NiIsImtpZCI6ImQwNTU5YzU5MDgzZDc3YWI2NDUxOThiNTIxZmM4ZmVmZmVlZmJkNjIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vd2lzZS1iYXRvbi0zNTM3MTAiLCJhdWQiOiJ3aXNlLWJhdG9uLTM1MzcxMCIsImF1dGhfdGltZSI6MTY3NDA3MzI5MCwidXNlcl9pZCI6IkFBcDM1RmdOT0dQNnBkaWg2M0JQRVJ0VGlrdTEiLCJzdWIiOiJBQXAzNUZnTk9HUDZwZGloNjNCUEVSdFRpa3UxIiwiaWF0IjoxNjc0MDczMjkwLCJleHAiOjE2NzQwNzY4OTAsImVtYWlsIjoiYWRtaW5AbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiYWRtaW5AbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.YUzajkfo59KwtD3lgipnpP1T1_QdOC56rk5IsCri1tFenhbdEdoxJA-NpsktA9snMadTiSDI0xqI-f84nYtnJAB_UhOGyF6qTsID06MuSP5pppuFLl8C9069JD6LFr6uVPc_K0P5m6CzQ5AjEQx2CLQ4_oeG4i_5CbFjqobdi5HeXUCfZymkz98KF8fEfBKQvmv-1jzRnCiU71Nt32t8zk-x8H933MKR_zNQWeRQSeLxnze7u6VqRBa6npYuS5hFH3pY2ZOMXOetOy9NgkZ8n9Ptpbkff-BcM9SGWyJWTfjgSd85ovYn6b6V4WrUVaZWUD6qtImhPFd20gJiZzudMQ",user_id="AAp35FgNOGP6pdih63BPERtTiku1")
        print(status)
    else:
        print("hello")
    return {'im working':"bitch"}

@app.route('/status')
def get_status():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=1212)
