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
email,password ="",""
app.secret_key = 'secret_word'


@app.route('/')
def index():
    return render_template("Login.html")


@app.route('/logout', methods=['POST'])
def logout():
    pass

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        login_data = request.get_json()
        email = login_data.get("email")
        password = login_data.get("password")
        try:
            print(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            print(user)
            return {"login":1}
        except:
            print("out")
            return {"login":0}

@app.route('/forgotpassword')
def forgot():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=1212)
