
####Import everything####
import os
import numpy as np
from flask import Flask,render_template,request
from werkzeug import secure_filename
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField,SelectField, StringField
import pybtex
from dominate.tags import img
from flask_sqlalchemy import SQLAlchemy
from flask_nav import Nav
from flask_bootstrap import Bootstrap
from flask_nav.elements import *
from pybtex.database import parse_file
import sqlite3

####Create app instance ####
app = Flask(__name__)

##Configure two FLask-SQLAlchemy configuration keys 
database_name = 'allbibs.db'
currentdir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(currentdir, database_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Create database object
database = SQLAlchemy(app)
connection = sqlite3.connect('allbibs.db')
sql_cmd ='''CREATE TABLE IF NOT EXISTS entries (ref_tag text,author_list text, journal text, volume integer, pages string, year integer, title string, collection string)'''

#execute query
cursor = connection.cursor()

####Encryption key####
app.config['SECRET_KEY'] = 'somerandomkey'

####Configure upload folder####
app.config['UPLOAD_FOLDER'] = 'uploads/uploaded_bibs'

##Create Bibs model###
class bibs(database.Model):
    __tablename__ = 'entries'
    #Define columns 
    id = database.Column(database.Integer, primary_key=True)

    ref_tag = database.Column(database.String)
    author_list = database.Column(database.String)
    journal = database.Column(database.String)
    volume = database.Column(database.Integer)
    pages = database.Column(database.String)
    year = database.Column(database.Integer)
    title = database.Column(database.String)
    collection = database.Column(database.String)
    

####Create class named registerbib ####
class register(FlaskForm):
    file = FileField("File", validators =[InputRequired()])
    submit = SubmitField("Insert Collection (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")


####Home page ####    
@app.route('/', methods=["GET","POST"]) 
def home():
    return render_template('home_page.html')

####Navigation page#### 
@app.route('/navpage')
def navpage():
    return render_template('navpage.html')

####Upload page####   
@app.route('/Upload', methods=["GET","POST"]) 

def registerbib():

    bib = register()
    
    if bib.validate_on_submit():
        #Store into file variable 
        file = bib.file.data 
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],file.filename))
        
        #Get user input name for collection
        form =request.form
       
        bib_info = parse_file(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],file.filename))
        
        for b in  bib_info.entries:

            authors = bib_info.entries[b].persons['author']
         
            entry = bibs(
                ref_tag = b,
                author_list = str(authors),
                journal = bib_info.entries[b].fields['journal'],
                volume = bib_info.entries[b].fields['volume'],
                pages = bib_info.entries[b].fields['pages'],
                year = bib_info.entries[b].fields['year'],
                title = bib_info.entries[b].fields['title'],
                collection = form['name'] )
            database.session.add(entry)
            database.session.commit()
        return 'Thanks for uploading the following collection: %s ' %( form['name'] ) 

    return render_template('template1.html', form=bib)

####Query page####  
@app.route('/RunQuery', methods=["GET","POST"]) 


def run_query():
    return render_template('template2.html')

#####Results page####
@app.route('/search', methods=["GET","POST"])     

def search():
    if request.method == "POST":
        inputs= request.form['search']
        connection = sqlite3.connect('allbibs.db')
        cursor = connection.cursor()
        
        query = """SELECT * FROM entries where %s """ %(inputs)
        cursor.execute(query)
        result = cursor.fetchall()

        return str(result) 
    

if __name__ == '__main__':
    app.run(debug=True)
