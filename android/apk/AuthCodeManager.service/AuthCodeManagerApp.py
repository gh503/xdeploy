#!/usr/bin/env python3
r"""APP service entrance provide sms code authentication manager.
Accept new sms from android phone installed AuthCodeManager App
and response the request from the client with authoried random token.

Since autotest scripts use the same phone number, the service doesnot
distinguish requests from different scripts. Then at the same time we
receive one new sms or send one sms code response. Once code sent, service
will clear the data.
"""
# -*- coding: utf-8 -*-


import json

from flask import Flask, request

from libs.Security import Security
from libs.SMSCode import SMSCode


app = Flask(__name__.split('.')[0])


@app.route('/', methods=['GET'])
def index():
    """Service Test"""
    return '''<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>ReadyForService</title>
        </head>
        <body>
            <h2>KunPeng PC APP Test by AuthCodeManager.service</h2>
            <p><b>Service goes well when you see this page.</b></p>
            <p>This service works for Kunpeng PC App Testing. World Peace!</p>
        </body>
    </html>'''


@app.route('/token', methods=['POST'])
def generate_token():
    """
    POST when:
    1. authoried client request new token
    request data:
        '{
            "username": username,
            "password": password,
            "phoneNumber": phoneNumber,
            "msg": message description
        }'
    """
    response = dict()
    client_data = json.loads(request.data)
    try:
        username = client_data['username']
        password = client_data['password']
        phone_num = client_data['phoneNumber']
        operate = client_data['operate']
    except KeyError:
        response['msg'] = 'fail!attributes including username,password,phoneNumber,operate expected!'
        response['status'] = 401
        return json.dumps(response)
    result = Security.auth_user(username, password, phone_num, operate)
    if result[0]:
        response['token'] = result[1]
        response['client'] = phone_num
        response['msg'] = 'success'
        response['status'] = 200
    else:
        response['client'] = phone_num
        response['msg'] = 'fail!invalid username, password or phoneNumber!'
        response['status'] = 401
    return json.dumps(response)


@app.route('/sms/new', methods=['POST'])
def add_sms():
    """process client sms post request

    POST when: client received a sms
    request data:
        {
            'token': client token
            'phoneNumber': client phone number
            'sms': sms content string
            'msg': message description
        }
    """
    response = dict()
    client_data = json.loads(request.data)
    try:
        client_token = client_data['token']
        phone_num = client_data['phoneNumber']
        sms = client_data['sms']
    except KeyError:
        response['msg'] = 'fail!attributes phoneNumber,token,sms expected!'
        response['status'] = 400
        return json.dumps(response)
    if Security.auth_token(client_token, phone_num):
        result = SMSCode.analyse(phone_num, sms)
        if result:
            response['msg'] = 'success'
            response['status'] = 200
        else:
            response['msg'] = 'fail to analyse sms content!'
            response['status'] = 400
    else:
        response['msg'] = 'fail!token error!'
        response['status'] = 401
    return json.dumps(response)


@app.route('/sms/app-latest', methods=['POST'])
def get_app_sms():
    """process client sms post request

    POST when: client require a sms code
    request data:
        {
            'token': client token
            'phoneNumber': client phone number
            'app': app name
            'msg': message description
        }
    """
    if request.method == 'POST':
        response = dict()
        client_data = json.loads(request.data)
        try:
            client_token = client_data['token']
            phone_num = client_data['phoneNumber']
            app_name = client_data['app']
        except KeyError:
            response['msg'] = 'fail!attributes phoneNumber,token,app expected!'
            response['status'] = 400
            return json.dumps(response)
        if Security.auth_token(client_token, phone_num):
            sms = SMSCode.get_app_sms(phone_num, app_name)
            if sms is None:
                response['msg'] = 'fail to get sms code.'
                response['status'] = 400
            else:
                response['msg'] = 'success'
                response['status'] = 200
                response['sms'] = sms
        else:
            response['msg'] = 'fail!token error!'
            response['status'] = 401
        return json.dumps(response, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True, host='192.18.1.3', port=50020)
