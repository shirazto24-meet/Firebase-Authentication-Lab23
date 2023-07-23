from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyDRa5Ivx-Az9YPibYY0HsQGXWqlwZcZRhs",
  "authDomain": "waterbottle-1ac10.firebaseapp.com",
  "projectId": "waterbottle-1ac10",
  "storageBucket": "waterbottle-1ac10.appspot.com",
  "messagingSenderId": "917953316977",
  "appId": "1:917953316977:web:15de65c998dd452059f3d0",
  "measurementId": "G-H255FGG9SS"
  "databaseURL":""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


@app.route('/', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)