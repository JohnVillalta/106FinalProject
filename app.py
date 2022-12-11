from flask import (
    Flask,
    render_template,
    request,
    session,
    url_for,
    redirect,
    g
)

app = Flask(__name__)

#this is the home page landing, this page gives you access to refreshing home page, accessing your profile if logged in
#logging in, and searching for other account profiles
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and request.form.get('home') == 'Home': #refresh home page
        return redirect(url_for('home'))
    if request.method == 'POST' and request.form.get('profile') == 'Profile': #access your own profile
        return redirect(url_for('profileSelf'))
    if request.method == 'GET' and request.args.get('search') != None: #access another profile and use search bar arguement as nameT
        nameT = request.args.get('searchBar')
        return redirect(url_for('profileOther', nameT=nameT))

    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
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
    return render_template('profileOther.html', nameT=nameT)

#directs you to your own profile if logged in, otherwise will lead to login page
@app.route('/profile-self', methods=['GET', 'POST'])
def profileSelf():
    if request.method == 'POST' and request.form.get('home') == 'Home': #redirect to home page landing
        return redirect(url_for('home'))
    if request.method == 'POST' and request.form.get('profile') == 'Profile': #refresh to your own page is signed in
        return redirect(url_for('profileSelf'))

    return render_template('profile.html')
