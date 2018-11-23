import json
import requests
from flask import Blueprint, redirect, current_app, request, jsonify


facebook_blueprint = Blueprint('facebook', __name__)


@facebook_blueprint.route('/social/facebook/oauth')
def oauth():
    base_url = current_app.config['FACEBOOK_OAUTH_URL']
    client_id = current_app.config['FACEBOOK_CLIENT_ID']
    redirect_uri = current_app.config['FACEBOOK_REDIRECT_URI']
    state = "{company={}}".format(1)

    url = '{}?client_id={}&redirect_uri={}&state={}'.format(
        base_url, client_id, redirect_uri, state)

    return redirect(url, code=302)


@facebook_blueprint.route('/social/facebook/access_token')
def access_token():
    base_url = current_app.config['FACEBOOK_ACCESS_TOKEN_URL']
    client_id = current_app.config['FACEBOOK_CLIENT_ID']
    client_secret = current_app.config['FACEBOOK_CLIENT_SECRET']
    code = request.args.get('code')

    print('*********CODE', code)

    url = '{}?client_id={}&redirect_url={}&client_secret={}&code={}'.format(
        base_url, client_id, client_secret, code)

    response = requests.get(url)
    data = json.loads(response.text)

    print('*********RESPONSE', data)

    return jsonify({
        'message': data,
        'data': data
    }), response.status_code
