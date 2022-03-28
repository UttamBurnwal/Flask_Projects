import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask import Flask, render_template, request, url_for, redirect

# The os module gives you access to miscellaneous operating system interfaces. 
# We can use it to construct a file path for our database.db database file.


# From the flask package, we then import the necessary helpers we need for our application: 
# the Flask class to create a Flask application instance, the render_template() function to 
# render templates, the request object to handle requests, the url_for() function to construct 
# URLs for routes, and the redirect() function for redirecting users. 


# We then import the SQLAlchemy class from the Flask-SQLAlchemy extension, 
# which gives us access to all the functions and classes from SQLAlchemy, in addition to 
# helpers, and functionality that integrates Flask with SQLAlchemy. We use it to create 
# a database object that connects to your Flask application, allowing us to create and manipulate 
# tables using Python classes, objects, and functions without needing to use the SQL language.


# We also import the func helper from the sqlalchemy.sql module to access SQL functions. 
# We’ll need it in our student management system to set a default creation date and time for 
# when a student record is created.


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
                                                                    

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100), nullable = False)
    last_name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    age = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime(timezone = True), server_default = func.now())
    bio = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Student {self.first_name}>'
    

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/<int:student_id>/')
def student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html', student = student) 

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method=='POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
        student = Student(first_name=first_name,
                          last_name=last_name,
                          email=email,
                          age=age,
                          bio=bio)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('create.html')

@app.route('/<int:student_id>/edit/', methods=('GET','POST'))
def edit(student_id):
    student = Student.query.get_or_404(student_id)
    
    if request.method=='POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
        
        student.first_name = first_name
        student.last_name = last_name
        student.email = email
        student.age = age
        student.bio = bio
        
        db.session.add(student)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('edit.html', student=student)

@app.post('/<int:student_id>/delete/')
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))