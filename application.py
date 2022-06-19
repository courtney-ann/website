import os
from json import loads
import bcrypt
from flask_login import LoginManager, login_required, current_user, logout_user
from bson.json_util import dumps
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request, session, render_template, url_for, flash
from datetime import timedelta
from flask_pymongo import PyMongo
from marshmallow import Schema, fields, ValidationError
from flask_cors import CORS
import bcrypt
import json

load_dotenv()

application = Flask(__name__)
CORS(application)
#setup location of database
application.config["MONGO_URI"] = os.getenv("MONGO_CONNECTION_STRING") 
mongo = PyMongo(application)
application.permanent_session_lifetime = timedelta(minutes = 30)
application.secret_key = os.getenv("secret")

class driverSchema(Schema):
    firstName = fields.String(required=True)
    lastName = fields.String(required=True)
    location= fields.String(required=True)
    time = fields.String(required=True)
    license = fields.String(required=True)
    status = fields.String(required=True)
    contact = fields.String(required=True)


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
        return render_template('drivers.html', list = driver_list)  
    else:
        return redirect(url_for('login'))



# Displays all drowsy drivers in the driver list collection
@application.route('/drowsy', methods = ['GET', 'POST'])
def drowsy():
        drowsy = mongo.db.drowsyList
        if 'username' in session:
            if request.method == 'GET':
                try:
                    list = drowsy.find()
                    drowsy_list = loads(dumps(list))
                    return render_template('drowsy.html', list = drowsy_list)

                except ValidationError as e:
                    return(e.messages, 400)
        else:
            return redirect(url_for('login'))    
        
        if 'username' in session:
            if request.method == 'POST':
                try: 
                    request_dict = request.json
                    
                except ValidationError as e:
                    return(e.messages, 400)
                new_driver = driverSchema().load(request_dict)
                driver_document = drowsy.insert_one(new_driver) #(mongo object)
                driver_id = driver_document.inserted_id
                driver = drowsy.find_one({"_id": driver_id})  #criterion is that id must be the id of the driver just inserted
                driver_json = loads(dumps(driver))
                jsonify(driver_json) 
                list = drowsy.find()
                drowsy_list = loads(dumps(list))
                jsonify(drowsy_list) 
        else:
            return redirect(url_for('login'))


# @application.route('/drowsy/<ObjectId:id>', methods = ['DELETE'])
# def delete_drowsy(id):
#     drowsy = mongo.db.drowsyList
#     if request.method == 'DELETE':
#         drowsy.delete_many({"_id":id,"status":"Awake"})
#         drowsy.delete_many({"_id":id,"status":"Accident"})
#         list = drowsy.find()
#         drowsy_list = loads(dumps(list))
#         return render_template('drowsy.html', list = drowsy_list) 


@application.route('/drowsy/<ObjectId:id>', methods = ['PATCH'])
def update_drowsy(id):
    drowsy = mongo.db.drowsyList
    request_dict = request.json 
    try: 
        driverSchema(partial=True).load(request_dict)
    except ValidationError as e:
        return(e.messages, 400)

    drowsy.update_one({"_id": id}, {"$set": request.json})
    driver = drowsy.find_one(id)
    driver_json = loads(dumps(driver))
    jsonify(driver_json)    
    list = drowsy.find()
    drowsy_list = loads(dumps(list))
    jsonify(drowsy_list) 
    return render_template('drowsy.html', list = drowsy_list)


# # Displays all accidents with drivers in the driver list collection
# @application.route('/accident', methods = ['GET','POST'])
# def accident():
#      accident = mongo.db.accidentList
#      if request.method == 'GET':
#         list = accident.find()
#         accident_list = loads(dumps(list))
#         return render_template('accident.html', list = accident_list)

#      if request.method == 'POST':
#             try: 
#                 request_dict = request.json
#             except ValidationError as err:
#                 return(err.messages, 400)
#             new_driver = driverSchema().load(request_dict)
#             accident_document = accident.insert_one(new_driver) #(mongo object)
#             driver_id = accident_document.inserted_id
#             driver = accident.find_one({"_id": driver_id})  #criterion is that id must be the id of the driver just inserted
#             driver_json = loads(dumps(driver))
#             jsonify(driver_json) 
#             list = accident.find()
#             accident_list = loads(dumps(list))
#             jsonify(accident_list)
#             return render_template('accident.html', list = accident_list)


# @application.route('/accident/<ObjectId:id>', methods = ['PATCH'])
# def update_accident(id):
#     accident = mongo.db.accidentList
#     request_dict = request.json 
#     try: 
#         driverSchema(partial=True).load(request_dict)
#     except ValidationError as err:
#         return(err.messages, 400)

#     accident.update_one({"_id": id}, {"$set": request.json})
#     driver = accident.find_one(id)
#     driver_json = loads(dumps(driver))
#     jsonify(driver_json)    
#     list = accident.find()
#     accident_list = loads(dumps(list))
#     jsonify(accident_list) 
#     return render_template('accident.html', list = accident_list)
  

# @application.route('/accident/<ObjectId:id>', methods = ['DELETE'])
# def delete_accident(id):
#     accident = mongo.db.accidentList
#     accident.delete_many({"id":id, "status":"Awake"})
#     accident.delete_many({"_id":id,"status":"Drowsy"})
#     list = accident.find()
#     accident_list = loads(dumps(list))
#     return render_template('accident.html', list = accident_list)

    

@application.route("/logout")
def logout():
    session.pop('username', None)
    # session.clear()
    flash("Logout successful")
    return redirect(url_for('login'))


if __name__ == "__main__":
    application.run(debug=True, port=3000, host="0.0.0.0")

