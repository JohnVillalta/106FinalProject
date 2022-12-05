from flask import (
    Flask,
    render_template,
    request,
    session,
    url_for
)
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method == 'POST':
    return render_template('login.html')
