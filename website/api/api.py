import yaml
import hmac
import hashlib

from flask import Flask, Response, request, redirect
from flask_cors import CORS
from concorde.integrations import Matrix
from matrix_client.errors import MatrixRequestError

app = Flask(__name__)
CORS(app)

config = yaml.load(open('config.yaml', 'r'))

HOMESERVER = config['homeserver']
PASSGEN_SECRET = config['passgen_secret']       # Used to generate passwords from mxid
MIGRATION_SECRET = config['migration_secret']   # Used to validate user was sent link by us

@app.route('/availability')
def availability():
    return 'I\'m here!'

@app.route('/claim', methods=['POST'])
def claim():
    content = request.get_json()
    mxid = content['mxid']
    code = content['code']
    new_password = content['password']

    if not request_is_valid(mxid, code):
        return '', 401

    matrix = Matrix(HOMESERVER)
    try:
        if matrix.claim_account(mxid, PASSGEN_SECRET, new_password):
            return 'success'
        return 'failure'
    except MatrixRequestError as exception:
        if exception.code == 403:
            return 'Unauthorized', 403
        else:
            return 'Unflubberized', exception.code

def request_is_valid(mxid, code):
    # Establish the validity of the request:
    mac = hmac.new(key=MIGRATION_SECRET,
                   digestmod=hashlib.sha1)
    mac.update(mxid)

    return mac.hexdigest() == code


if __name__ == '__main__':
    app.run()
