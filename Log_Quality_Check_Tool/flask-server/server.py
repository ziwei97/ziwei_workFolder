from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, unset_jwt_cookies, jwt_required, get_jwt_identity
import os
from flask_cors import CORS
from io import BytesIO
import pandas as pd
import numpy as np
from bson import ObjectId
from datetime import timedelta
from pymongo import MongoClient
from waitress import serve

app = Flask(__name__, static_folder='../react-client/build/static', template_folder="../react-client/build")
CORS(app)

client = MongoClient('mongodb', 27017)
result_scheme = client["ReportView"]

uploads = os.path.join(app.root_path, 'uploads') 
admin_hash = generate_password_hash("Texas512")
user_hash = generate_password_hash("apple")
JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.urandom(16)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=45)

def insertDF(df):
    dict_data = df.to_dict("records")
    result_scheme["Records"].insert_many(dict_data)  

@app.route("/")
def hello():
    return render_template('index.html')

@app.errorhandler(404)   
def not_found(e):   
  return render_template('index.html')

@app.route('/getReports')
@jwt_required()
def getReports():
    data = list(result_scheme["Records"].find({}))
    for item in data:
        item['_id'] = str(item['_id'])
    headers = list(data[0].keys()) if len(data) > 0 else []
    headers = list(filter(lambda x: x != '_id', headers))
    col = list(map(lambda x: {'Header': x, 'accessor': x}, headers))
    return {"row": data, "col": col}

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token, roles=identity)

@app.route('/login', methods = ["POST"])
def login():
    body = request.get_json()
    username = body['username']
    password = body['password']
    if username == "admin" and check_password_hash(admin_hash, password):
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return {
            'access_token': access_token,
            'roles': 'admin',
            'refresh_token': refresh_token
            }
    if username == "user" and check_password_hash(user_hash, password):
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return {
            'access_token': access_token,
            'roles': 'user',
            'refresh_token': refresh_token
            }
    return {"msg": "Wrong email or password"}, 401

@app.route("/logout", methods = ["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@app.route("/uploadFilesLocal", methods = ["POST"])
@jwt_required()
def uploadFilesLocal():
    all_files = request.files.getlist("files[]")
    msg = []
    for file in all_files:
        try:
            df = pd.read_csv(BytesIO(file.read()))
        except:
            msg.append("Invalid file type")
        else:
            df = df.replace({np.nan: None})
            insertDF(df)
            msg.append("added successfully")
    return {"msg": msg}

@app.route("/uploadReport", methods = ["POST"])
@jwt_required()
def uploadReport():
    msg = []
    row_id = request.form['object_id']
    all_files = request.files.getlist("files[]")
    for file in all_files:
        if file.filename[-4:] != ".pdf":
            msg.append("Invalid file type")
        else:
            file.save(uploads + "/" + row_id + ".pdf")
            result_scheme["Records"].update_one({
                    '_id': ObjectId(row_id)
                },{
                '$set': {
                    "report": 1
                }
            }, upsert=False)
            msg.append("added successfully")
    return {"msg": msg}

@app.route("/downloadReport/<filename>")
@jwt_required()
def downloadReport(filename):
    filename = filename + ".pdf"
    return send_from_directory(uploads, filename, as_attachment=True)


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5070)
    # app.run(host='0.0.0.0', port=8000, debug=True)
