from flask import Flask, render_template, request, session, redirect
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
app.secret_key='super-secret-key'

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
class Posts(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String(250), nullable=False)
    slug =db.Column(db.String(50),nullable=False)
    content= db.Column(db.String(300),nullable=False)
    img_post= db.Column(db.String(50),nullable=True)
    date= db.Column(db.String(50),nullable=True)

#this is additional for check database is connect or not
from sqlalchemy import text

@app.before_request
def test_connection():
    try:
        db.session.execute(text('SELECT 1'))
        print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {e}")

# Define a custom filter to truncate text to a number of words
@app.template_filter('truncate_words')
def truncate_words(text, num_words):
    words = text.split()
    return ' '.join(words[:num_words])


@app.route("/")
def index():
    posts=Posts.query.filter_by().all()
    return render_template("index.html",params=params,posts=posts)

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
        return redirect(url_for('/contact'))


    return render_template("contact.html",params=params)

@app.route('/single-post')
def single_post():
    return render_template("single-post.html",params=params)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post(post_slug):
    post_data=Posts.query.filter_by(slug=post_slug).first()
    print(post_data)
    return render_template("post.html",params=params, post_data=post_data)


@app.route('/starter-page')
def starter():
    return render_template("starter-page.html",params=params)


@app.route('/Dashbord', methods=['GET','POST'])
def Dashboard():
    if ('user' in session and session['user']==params['admin_email']):
        posts=Posts.query.all()

        return render_template("dashboard.html",params=params,posts=posts)
    

    if request.method =="POST":
        useremail=request.form.get("email")
        userpassword=request.form.get("password")
        if (useremail == params['admin_email'] and userpassword == params['admin_password']):
            #session variable decleration
            session['user']=useremail
            posts=Posts.query.all()
            return render_template("dashboard.html",params=params,posts=posts)
    
    return render_template("adminlogin.html",params=params)

#this function is Add a Post with the help of Dashboard
@app.route('/Addpost',methods=['GET','POST'])
def Addpost():
    if 'user' in session and session['user']==params['admin_email']:
        if request.method == 'POST':
            title=request.form.get('title')
            slug=request.form.get('slug')
            content=request.form.get('content')
            img_post=request.form.get('img_post')
            date=datetime.now()

            post=Posts(title=title,slug=slug,content=content,img_post=img_post,date=date)
            db.session.add(post)
            db.session.commit()
            return redirect('/Dashbord')

@app.route('/deletepost/<int:id>',methods=['POST'])
def delete_post(id):
    post = Posts.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/Dashbord')

    

@app.route('/updatepost', methods=['POST'])
def updatepost():
    post_id = request.form.get('id')  # Get post ID from hidden input
    print(post_id)
    post = Posts.query.get_or_404(post_id)

    post.title = request.form['title']
    post.slug = request.form['slug']
    post.content = request.form['content']
    post.img_post = request.form['img_post']

    db.session.commit()    
    db.session.rollback()
        
    return redirect('/Dashbord')
            
@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/Dashbord')




app.run(debug=True)