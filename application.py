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
import bcrypt


load_dotenv()

application = Flask(__name__)
CORS(application)
#setup location of database
application.config["MONGO_URI"] = os.getenv("MONGO_CONNECTION_STRING") 
mongo = PyMongo(application)

application.permanent_session_lifetime = timedelta(minutes = 10)
application.secret_key = os.getenv("secret")


class driverSchema(Schema):
    firstName = fields.String(required=True)
    lastName = fields.String(required=True)
    location= fields.String(required=True)
    time = fields.String(required=True)
    license = fields.String(required=True)
    status = fields.String(required=True)
    contact = fields.String(required=True)

driver = {
    "firstName": "Courtney-Ann",
    "lastName": "Hanson",
    "location": "77N 18W",
    "time": "6:45:22 AM",
    "license": "JA876",
    "status": "Awake",
    "contact": "876-331-7440"
}

@application.route('/home', methods = ['GET'])
def home():
    return render_template('home.html')


@application.route('/contact', methods = ['GET'])
def contact():
    return render_template('contact.html')


@application.route('/about', methods = ['GET'])
def about():
    return render_template('about.html')


@application.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':
         users = mongo.db.admin
         Admin = users.find_one({'username': request.form['nm']})
         if Admin:
            if request.form['pw'] == Admin['password']:
                session['username'] = request.form['nm']
                flash("Login succesful!")
                return redirect(url_for('home')) 

            else:
                flash("Login unsuccesful")
                return redirect(url_for('login'))

    elif request.method == "GET":
         return render_template('login.html')
    

# Displays all drivers in the driver list collection
@application.route('/drivers', methods = ['GET'])       
def drivers():
    drivers = mongo.db.driverList
    if 'username' in session:
        list = drivers.find()
        driver_list = loads(dumps(list))
        #return jsonify(driver_list)         
        return render_template('drivers.html', list = list)
    else:
        return redirect(url_for('login'))

# Displays all drowsy drivers in the driver list collection
@application.route('/drowsy', methods = ['GET', 'POST', 'PATCH', 'DELETE'])
def drowsy():
        drivers = mongo.db.driverList
        if request.method == 'GET':
            if 'username' in session:
                list = drivers.find()
                driver_list = loads(dumps(list))
                #return jsonify()       #list of drowsy drivers
                return render_template('drowsy.html')
            else:
                return redirect(url_for('login'))

# Displays all accidents with drivers in the driver list collection
@application.route('/accident', methods = ['GET',' POST', 'PATCH', 'DELETE'])
def accident():
     if 'username' in session:
        return render_template('accident.html')
     else:
        return redirect(url_for('login'))

@application.route("/logout")
def logout():
    session.pop('username', None)
    flash("Logout successful")
    return redirect(url_for('login'))


if __name__ == "__main__":
    application.run(debug=True, port=3000, host="0.0.0.0")
