#6C/19090124/Syahrul Adi Mustofa
#6C/19090100/Eria Rahmadhani

#import library
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

import jwt
import os
import datetime

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
CORS(app)

#dbcon
filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'syhrl.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = "syhrl6C"

#dbtablesett
class AuthModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
db.create_all()

#loginsession
class Login(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        queryUsername = [data.username for data in AuthModel.query.all()]
        queryPassword = [data.password for data in AuthModel.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword:
            
            return make_response(jsonify({"Welcome " : dataUsername}), 200)
        return jsonify({"Msg ":"Login Gagal, Coba Lagi"}) 

#infouserGETusernameAndpassword
class infouser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        queryUsername = [data.username for data in AuthModel.query.all()]
        queryPassword = [data.password for data in AuthModel.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword:
            token = jwt.encode(
                {
                    "username":queryUsername, 
                    "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
                }, app.config['SECRET_KEY'], algorithm="HS256"
            )
            return make_response(jsonify({"Token API":token}), 200)
        return jsonify({"Msg ":"Gagal Mengambil Info"}) 
   
#api.add_resource(RegisterUser, "/reg", methods=["POST"])
#api.add_resource(LoginUser, "/log", methods=["POST"])

api.add_resource(Login, "/api/v1/login", methods=["POST"])
api.add_resource(infouser, "/api/v2/users/info", methods=["POST"])


if __name__ == "__main__":
    app.run(port=2001, debug=True)
