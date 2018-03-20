import yaml
import json
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
    mxid = content['mxid'] if 'mxid' in content else ''
    code = content['code'] if 'code' in content else ''
    new_password = content['password']

    if not request_is_valid(mxid, code):
        return json.dumps({
            'response_code': 401,
            'message': 'Your request to claim this account could not be validated - please speak to your community administrator.',
            'error': 'CODE_VALIDATION_FAILURE'
            })

    matrix = Matrix(HOMESERVER)
    try:
        if matrix.claim_account(mxid, PASSGEN_SECRET, new_password):
            return json.dumps({
                'response_code': 200,
                'message': 'Your account has been successfully claimed!'
                })
        return json.dumps({
            'response_code': 401,
            'message': 'This account already seems to have been claimed - please speak to your community administrator.',
            'error': 'PASSWORD_ALREADY_RESET'
            })
    except MatrixRequestError as exception:
        if exception.code == 403:
            return json.dumps({
                'response_code': 404,
                'message': 'This account already seems to have been claimed - please speak to your community administrator.',
                'error': 'PASSWORD_ALREADY_RESET'
                })
        else:
            return json.dumps({
                'response_code': exception.code,
                'message': 'This request failed - please try again later.',
                'error': 'GENERIC_FAILURE'
                })

def request_is_valid(mxid, code):
    # Establish the validity of the request:
    if mxid == '' or code == '':
        return False

    mac = hmac.new(key=MIGRATION_SECRET,
                   digestmod=hashlib.sha1)
    mac.update(mxid)

    return mac.hexdigest() == code


if __name__ == '__main__':
    app.run()
