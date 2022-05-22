import os
from json import loads
import bcrypt
from bson.json_util import dumps
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request, session, render_template, url_for, flash
from datetime import timedelta
from flask_pymongo import PyMongo
from marshmallow import Schema, fields, ValidationError
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
CORS(app)
#setup location of database
app.config["MONGO_URI"] = os.getenv("MONGO_CONNECTION_STRING") 
mongo = PyMongo(app)

app.permanent_session_lifetime = timedelta(minutes = 5)
app.secret_key = os.getenv("secret")

class credSchema(Schema):
    user = fields.String(required = True)
    pw = fields.String(required = True)

class driverSchema(Schema):
    firstName = fields.String(required=True)
    lastName = fields.String(required=True)
    location= fields.String(required=True)
    time = fields.DateTime(required=True)
    id = fields.String(required=True)
    license = fields.String(required=True)
    status = fields.String(required=True)
    contact = fields.String(required=True)


@app.route('/home', methods = ['GET'])
def home():
    return render_template('home.html')


@app.route('/contact', methods = ['GET'])
def contact():
    return render_template('contact.html')


@app.route('/about', methods = ['GET'])
def about():
    return render_template('about.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':
         users = mongo.db.users
         Admin = users.find_one({'username': request.form['nm']})
         if Admin:
            if bcrypt.hashpw(request.form['pw'].encode('utf-8'), Admin['password'].encode('utf-8')) == Admin['password'].encode('utf-8'):
                session['username'] = request.form['nm']
                flash("Login succesful!")
                return redirect(url_for('home')) 

            else:
                flash("Login succesful!")
                #return redirect(url_for('home'))

    # if request.method == 'POST':     
    #     if request.form['nm'] != 'admin' and request.form['pw'] != 'admin':
    #        flash("Invalid Credentials")
    #       # return redirect(url_for('login'))
    #        return render_template('login.html')

    #     elif request.form['nm'] == 'admin' and request.form['pw'] == 'admin':
    #         return redirect(url_for('home'))

    elif request.method == "GET":
         return render_template('login.html')
    

@app.route('/drivers', methods = ['GET',' POST', 'PATCH', 'DELETE'])
def drivers():
    return render_template('drivers.html')


@app.route('/drowsy', methods = ['GET',' POST', 'PATCH', 'DELETE'])
def drowsy():
    return render_template('drowsy.html')


@app.route('/accident', methods = ['GET',' POST', 'PATCH', 'DELETE'])
def accident():
    return render_template('accident.html')


@app.route("/logout")
def logout():
    session.pop('nm', None)
    flash("Logout successful")
    return redirect(url_for('login'))


if __name__ == "__main__":
  app.run(debug=True, port=3000, host="0.0.0.0")
