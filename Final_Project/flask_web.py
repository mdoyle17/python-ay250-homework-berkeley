
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
import pickle
import h5py
from PIL import Image

def unique(list1):
    # initialize a null list
    unique_list = []
     
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    all_unique = []
    for x in unique_list:
        all_unique.append(x)
    return all_unique

def Reverse(lst):
    return [ele for ele in reversed(lst)]

####Create app instance ####
app = Flask(__name__)

model = pickle.load(open('model.pkl','rb'))

hf = h5py.File('train_data.h5', 'r')

labels = hf['label'][()]
options = unique(labels)
#execute query


####Encryption key####
app.config['SECRET_KEY'] = 'randomkey'

####Configure upload folder####
app.config['UPLOAD_FOLDER'] = 'uploads/'

class register(FlaskForm):
    file = FileField("File", validators =[InputRequired()])
    submit = SubmitField("Insert Spectra for Prediction")

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

    
def register_spectra():

    bib = register()
    
    if bib.validate_on_submit():
        #Store into file variable 
        file = bib.file.data 
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],file.filename))
        
        img = np.load(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],file.filename))
        
        prediction=model.predict(img)
     
        
        img_for_display = Image.fromarray((img[0]).astype(np.uint8))
        img_for_display.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],'temp.png'))
        
        
        return_string =[]
        for x in range(0,len(prediction[0])):
            return_string.append('%s percent chance of being %s' %((prediction[0][x])*100, options[x]) )
        
        #Now want to sort results ... 
        updated=[]
        for y in return_string:
            i =y.split(" ")
            i[0] = float(i[0])
            updated.append(i)
            
        new_idx = [i[0] for i in sorted(enumerate(updated), key=lambda x:x[1])]
        
        
        return render_template('template2.html', data=Reverse(np.array(return_string)[new_idx]))
    return render_template('template1.html', form=bib)


    
    
if __name__ == '__main__':
    app.run(debug=True, port=9000)
