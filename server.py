# Souvenir Server v0.1
# Écrit par Alejandro Garcia
#
from pymongo import MongoClient
from flask import Flask, request, Response, send_file
from flask_httpauth import HTTPBasicAuth
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

    filename = request.args.get('title')
    collection = request.args.get('collection')
    memo = request.files['file']

    save_filename = collection + '_' + filename
    memo.save(os.getcwd() + '/audios/' + save_filename)

    save_col = database[collection]

    file = {'filename': filename,
            'save_name': save_filename}

    save_col.insert_one(file)

    return Response(response='Uploaded!\n', status=201, mimetype='text')


@app.route('/download')
@auth.login_required()
def download():

    filename = request.args.get('title') + '.wav'
    collection = request.args.get('collection')
    save_filename = collection + '_' + filename
    save_col = database[collection]

    if save_col.find_one({'filename': filename, 'save_name': save_filename}):
        return send_file(os.getcwd() + '/audios/' + save_filename, as_attachment=True)
    else:
        return Response('File not found\n', status=404, mimetype='text')


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
    if not os.path.exists(os.getcwd() + '/audios'):
        os.mkdir(os.getcwd() + '/audios')
    app.run('0.0.0.0', port=19720, debug=True)
