from flask import Flask, request, render_template, session, redirect
import pyrebase

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

app.secret_key = 'secret_word'


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("Login.html")


@app.route('/logout')
def logout():
    pass

@app.route('/login')
def login():
    return {"userId": ["hello", "hi", "try"],}

@app.route('/forgotpassword')
def forgot():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=1212)
