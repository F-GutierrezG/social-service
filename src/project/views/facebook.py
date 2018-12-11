from flask import Blueprint, request, jsonify

from auth.decorators import authenticate
from project.logics import FacebookLogics


facebook_blueprint = Blueprint('facebook', __name__)


@facebook_blueprint.route('/social/facebook/oauth/<company_id>')
@authenticate
def oauth(user, company_id):
    url = FacebookLogics().oauth(user, company_id)
    return jsonify({
        'message': 'facebook oauth url',
        'data': url
    }), 200


@facebook_blueprint.route('/social/facebook/access_token')
def access_token():
    code = request.args.get('code')
    state = request.args.get('state')

    response, data = FacebookLogics().access_token(code, state)

    return jsonify({
        'message': data,
        'data': data
    }), response.status_code
