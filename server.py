# Souvenir Server v0.1
# Écrit par Alejandro Garcia
#
from pymongo import MongoClient
from flask import Flask, request, Response, send_file
from flask_httpauth import HTTPBasicAuth
import gridfs
import os

# Basic Flask, HTTPAuth, MongoDB setup
app = Flask(__name__)
auth = HTTPBasicAuth()
client = MongoClient()
database = client['Souvenir']
user_col = database['user_auth']


@app.route('/login')
@auth.login_required()
def check_login():
    return Response(response='Valid credentials\n', status=200, mimetype='text')


@app.route('/upload', methods=['POST'])
@auth.login_required()
def save_file():

    memo = request.files['file']
    memo.save(os.getcwd() + '/' + memo.filename)


@app.route('/download')
@auth.login_required()
def download():
    return False


@app.route('/list', methods=['GET'])
@auth.login_required()
def retrieve_file():

    filelist = []
    return filelist


# Verify password through mongodb
@auth.verify_password
def verify_password(username, password):
    if user_col.find_one({'username': username, 'password': password}):
        return username


# Error handling function
@auth.error_handler
def auth_error():
    return Response(response='Error: Invalid login.', status=401, mimetype='text')


if __name__ == '__main__':
    app.run('0.0.0.0', port=19720)
