# coding=utf-8
"""Matrix side of the Slack migrator."""

import json
import hmac
import hashlib
import requests

from matrix_client.client import MatrixClient

def passgen(mxid, passgen_secret):
    """Function for translating a mxid into a known-but-unguessable password."""
    return hashlib.sha256(mxid + '\x00' + passgen_secret).hexdigest()

class Matrix(object):
    """For wrangling the Matrix users."""

    def __init__(self, server):
        self._server = server

    def create_account(self, server_secret, mxid, passgen_secret, password_function=passgen, admin=False):
        """Creates a user - the password is generated from a function."""

        mac = hmac.new(key=server_secret,
                       digestmod=hashlib.sha256)

        password = password_function(mxid, passgen_secret)

        mac.update(mxid)
        mac.update("\x00")
        mac.update(password)
        mac.update("\x00")
        mac.update("admin" if admin else "notadmin")

        body = {
            "user": mxid,
            "password": password,
            "mac": mac.hexdigest(),
            "type": "org.matrix.login.shared_secret",
            "admin": admin, # XXX: What does this even do?
        }

        response = requests.post('%s/_matrix/client/api/v1/register' % self._server,
                                 data=json.dumps(body),
                                 headers={'Content-Type': 'application/json'})

        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        else:
            return True

    def claim_account(self, mxid, passgen_secret, new_password, display_name=None,
                      password_function=passgen):
        """Claims an account by logging in with the genned password, setting a display
        name, and changing the password to a new password."""
        matrix = MatrixClient(self._server)

        old_password = password_function(mxid, passgen_secret)
        matrix.login_with_password_no_sync(username=mxid,
                                           password=old_password)

        if display_name:
            matrix.api.set_display_name(matrix.user_id, display_name)

        body = {
            "auth": {
                "type": "m.login.password",
                "user": mxid,
                "password": old_password
            },
            "new_password": new_password
        }

        matrix.api._send('POST', '/account/password', body, api_path='/_matrix/client/r0')
        return True
