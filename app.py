from flask import (
    Flask,
    render_template,
    request,
    session,
    url_for,
    redirect,
    g,
    flash,
)
from flask_login import LoginManager #,UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)


login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = "login"

#@login_manager.user_loader
#def load_user(user_id):
    #return Users.query.get(int(user_id))


#this is the home page landing, this page gives you access to refreshing home page, accessing your profile if logged in
#logging in, and searching for other account profiles
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and request.form.get('home') == 'Home': #refresh home page
        return redirect(url_for('home'))
    if request.method == 'POST' and request.form.get('profile') == 'Profile': #access your own profile
        return redirect(url_for('profileSelf'))
    if request.method == 'POST' and request.form.get('sign') == 'Sign in':
        return redirect(url_for('login'))
    if request.method == 'GET' and request.args.get('search') != None: #access another profile and use search bar arguement as nameT
        nameT = request.args.get('searchBar')
        return redirect(url_for('profileOther', nameT=nameT))

    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    return render_template('signUp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    #form = LoginForm()
    #if form.validate_on_submit():
        #login_user(user)
        #flask.flash('Logged in successfully')
    # if request.method == 'POST':
    return render_template('login.html')

#this must always have nameT as a parameter since we're using that to find the profile, future implementation could use
#user.ID or something of the sort :)
@app.route('/profile-other/<nameT>', methods=['GET', 'POST'])
def profileOther(nameT):
    if request.method == 'POST' and request.form.get('home') == 'Home': #redirect to home page landing
        return redirect(url_for('home'))
    if request.method == 'POST' and request.form.get('profile') == 'Profile': #redirect to your own page if signed in
        return redirect(url_for('profileSelf'))
    if request.method == 'GET' and request.args.get('search') != None: #access another profile and use search bar arguement as nameT
        nameT2 = request.args.get('searchBar')
        return redirect(url_for('profileOther', nameT=nameT2))

    return render_template('profileOther.html', nameT=nameT)

#directs you to your own profile if logged in, otherwise will lead to login page
@app.route('/profile-self', methods=['GET', 'POST'])
def profileSelf():
    if request.method == 'POST' and request.form.get('home') == 'Home': #redirect to home page landing
        return redirect(url_for('home'))
    if request.method == 'POST' and request.form.get('profile') == 'Profile': #refresh to your own page is signed in
        return redirect(url_for('profileSelf'))
    if request.method == 'GET' and request.args.get('search') != None: #access another profile and use search bar arguement as nameT
        nameT = request.args.get('searchBar')
        return redirect(url_for('profileOther', nameT=nameT))

    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)