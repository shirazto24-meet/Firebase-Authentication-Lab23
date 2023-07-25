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
  "measurementId": "G-H255FGG9SS",
  "databaseURL":"https://waterbottle-1ac10-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


@app.route('/', methods=['GET', 'POST'])
def signin():
    error= ""
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('add_tweet'))
        except:
            error = 'signin failed'
            return render_template("signin.html")
    else:
        return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error= ""
    if request.method == 'POST':
        email= request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']

        

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)

            UID = login_session['user']['localId']
            user = {"email":email,"password":password,"full_name":full_name,"username": username,"bio":bio }
            db.child("Users").child(UID).set(user)
            return redirect(url_for('signin'))
        except:
            error = "auth failed"
            return render_template("signup.html")
    else:
        return render_template('signup.html')


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    try:
        UID = login_session['user']['localId']
    except:
        return redirect(url_for("signin"))

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        
        tweet = {'title':title, 'text':text,'uid':UID}
        db.child('Tweets').push(tweet)
        return redirect(url_for("all_tweets"))


    else:
        return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    tweets = db.child("Tweets").get().val()
    return render_template("tweets.html", tweets=tweets)


if __name__ == '__main__':
    app.run(debug=True)