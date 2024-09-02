# from flask import Flask, render_template,request
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app= Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:@localhost/Shivam_Blog'
# db=SQLAlchemy(app)

# class Contacts(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100), nullable=False)
#     Email = db.Column(db.String(100), nullable=False)
#     phone = db.Column(db.String(100), nullable=False)
#     Message = db.Column(db.String(300), nullable=False)
#     Date = db.Column(db.DateTime, nullable=True)  # Changed to DateTime
#     Phone = db.Column(db.String(15), nullable=False)  # Added phone column

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route('/about')
# def about():
#     return render_template("about.html")

# @app.route('/category')
# def category():
#     return render_template("category.html")

# @app.route('/contact',  methods=['GET', 'POST'])
# def contact():
#     if(request.method=='POST'):
#         name=request.form.get('name')
#         email=request.form.get('email')
#         phone=request.form.get('phone')
#         message=request.form.get('message')

#         entry=Contacts(Name=name,Email=email,phone=phone,Message=message,Date=datetime.now())
#         db.session.add(entry)
#         db.session.commit()





#     return render_template("contact.html")

# @app.route('/single-post')
# def single_post():
#     return render_template("single-post.html")

# @app.route('/starter-page')
# def starter():
#     return render_template("starter-page.html")

# app.run(debug=True)


from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

# Use PyMySQL as MySQLdb
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/Shivam_Blog'
db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    Message = db.Column(db.String(300), nullable=False)
    Date = db.Column(db.DateTime, nullable=True)  # Changed to DateTime
    Phone = db.Column(db.String(15), nullable=False)  # Added phone column

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/category')
def category():
    return render_template("category.html")

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
        

    return render_template("contact.html")

@app.route('/single-post')
def single_post():
    return render_template("single-post.html")

@app.route('/starter-page')
def starter():
    return render_template("starter-page.html")

app.run(debug=True)
