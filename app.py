from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
from flask import redirect, url_for
import json

# Use PyMySQL as MySQLdb
pymysql.install_as_MySQLdb()



with open('config.json','r') as c:
    params=json.load(c)["parameters"]

local_server=True
app = Flask(__name__)

if local_server:

    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Phone = db.Column(db.String(100), nullable=False)
    Message = db.Column(db.String(300), nullable=False)
    Date = db.Column(db.DateTime, nullable=True)  # Changed to DateTime
    #Phone = db.Column(db.String(15), nullable=False)  # Added phone column

@app.route("/")
def index():
    return render_template("index.html",params=params)

@app.route('/about')
def about():
    return render_template("about.html",params=params)

@app.route('/category')
def category():
    return render_template("category.html",params=params)

@app.route('/contact', methods=['GET', 'POST'])  # Corrected to methods
def contact():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        print(name)
        entry = Contacts(Name=name, Email=email, Phone=phone, Message=message, Date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('contact'))


    return render_template("contact.html",params=params)

@app.route('/single-post')
def single_post():
    return render_template("single-post.html",params=params)

@app.route('/starter-page')
def starter():
    return render_template("starter-page.html",params=params)

app.run(debug=True)
