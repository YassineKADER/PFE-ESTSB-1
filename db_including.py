import pyrebase

config = {
    "apiKey": "",
    "authDomain": "wise-baton-353710.firebaseapp.com",
    "databaseURL": "",
    "projectId": "wise-baton-353710",
    "storageBucket": "wise-baton-353710.appspot.com",
    "messagingSenderId": "962857669223",
    "appId": "1:962857669223:web:3360987f13c2f1e6787ac2"
}



firebase = pyrebase.initialize_app(config)

db = firebase.database()
auth = firebase.auth()

data2 = {
    "Name": "morade kad",
    "Phone": "+212613248324",
    "Message": "Say hi !"
}

data4 = db.child("Users").get()

print(data4.val())

email = "yassine.kader2017fc@gmail.com"
password = "password2023"
#user = auth.create_user_with_email_and_password(email, password) #to create a new user

user = auth.sign_in_with_email_and_password(email, password)
data = auth.current_user #get the user data
print(user)

send_reset_mail = auth.send_password_reset_email("yassine.kader2017fc@gmail.com")

data = {
    "name":"e",
    "lastname" : "kar",
    "age" : 19,
    "alive" : True
}

db.child("Users").child(user["localId"]).set(data, token=user['idToken'])

print(db.api_key)
