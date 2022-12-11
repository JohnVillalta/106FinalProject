from flask import (
    Flask,
    render_template,
    request,
    session,
    url_for,
    redirect
)

app = Flask(__name__)
nameT = ''

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and request.form.get('home') == 'Home':
        return redirect(url_for('home'))
    if request.method == 'POST' and request.form.get('profile') == 'Profile':
        return redirect(url_for('profileSelf'))
    if request.method == 'POST' and request.form.get('search') == 'Search':
        nameT = request.form.get('searchBar')
        return redirect(url_for('profileOther', nameT=nameT))

    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method == 'POST':
    return render_template('login.html')

@app.route('/profile-other', methods=['GET', 'POST'])
def profileOther():
    if request.method == 'POST' and request.form.get('home') == 'Home':
        return redirect(url_for('home'))
    return render_template('profileOther.html', nameT=nameT)

@app.route('/profile-self', methods=['GET', 'POST'])
def profileSelf():
    if request.method == 'POST' and request.form.get('home') == 'Home':
        return redirect(url_for('home'))
    if request.method == 'POST' and request.form.get('profile') == 'Profile':
        return redirect(url_for('profile'))

    return render_template('profile.html')
