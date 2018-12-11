from flask import Blueprint, request

from auth.decorators import authenticate
from project.logics import PublicationLogics
from project.views.utils import success_response


publications_blueprint = Blueprint('publications', __name__)


@publications_blueprint.route('/social/publications', methods=['POST'])
@authenticate
def create(user):
    publication_data = {}
    publication_data['company_id'] = 1
    publication_data['date'] = request.form.get('date')
    publication_data['time'] = request.form.get('time')
    publication_data['social_networks'] = request.form.get(
        'social_networks').split(',')
    publication_data['message'] = request.form.get('message')
    publication_data['image'] = request.files.get('image')
    publication_data['created_by'] = user.id

    publication = PublicationLogics().create(publication_data)

    return success_response(
        data=publication,
        status_code=201)