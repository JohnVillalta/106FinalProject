from flask import (
    Flask,
    render_template,
    request,
    session,
    url_for,
    redirect,
    g,
    flash,
    current_app
)
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'saltines'
app.app_context().push

db = SQLAlchemy(app)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    blogs = db.relationship('Blog', lazy='select', backref=db.backref('user', lazy='joined'))

class Blog(db.Model, UserMixin):
    blogId = db.Column(db.Integer, primary_key=True)
    userId =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blogString = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

class SignUpForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Username'})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Password'})
    submit = SubmitField('SignUp')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Username'})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Password'})
    submit = SubmitField('Login')

with app.app_context():
    db.create_all()

#login_manager.init_app(app)
#login_manager.login_view = "login"

#@login_manager.user_loader
#def load_user(user_id):
    #return Users.query.get(int(user_id))

#@app.teardown_request
#def show_teardown(exception):
    #print('after with block')

#with app.test_request_context():
    #print('during with block')

#this is the home page landing, this page gives you access to refreshing home page, accessing your profile if logged in
#logging in, and searching for other account profiles
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and request.form.get('home') == 'Home': #refresh home page
        return redirect(url_for('home'))
    if request.method == 'POST' and request.form.get('profile') == 'Profile': #access your own profile
        return redirect(url_for('profileSelf'))
    if request.method == 'POST' and request.form.get('sign') == 'Sign In':
        return redirect(url_for('login'))
    if request.method == 'GET' and request.args.get('search') != None: #access another profile and use search bar arguement as nameT
        nameT = request.args.get('searchBar')
        return redirect(url_for('profileOther', nameT=nameT))

    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    form = SignUpForm()
    return render_template('signUp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
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