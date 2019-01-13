from flask import Blueprint, request

from auth.decorators import authenticate
from project.logics import PublicationLogics, BadRequest, NotFound
from project.views.utils import success_response, failed_response


publications_blueprint = Blueprint('publications', __name__)


@publications_blueprint.route('/social/publications', methods=['POST'])
@authenticate
def create(user):
    publication_data = {}
    publication_data['company_id'] = 1
    publication_data['date'] = request.form.get('date')
    publication_data['time'] = request.form.get('time')
    publication_data['title'] = request.form.get('title')
    publication_data['social_networks'] = request.form.get(
        'social_networks').split(',')
    publication_data['message'] = request.form.get('message')
    publication_data['additional'] = request.form.get('additional')
    publication_data['image'] = request.files.get('image')
    publication_data['created_by'] = user.id

    publication = PublicationLogics().create(publication_data)

    return success_response(
        data=publication,
        status_code=201)


@publications_blueprint.route('/social/publications', methods=['GET'])
@authenticate
def list(user):
    publications = PublicationLogics().list(user)

    return success_response(
        data=publications,
        status_code=200)


@publications_blueprint.route(
    '/social/publications/<id>/reject', methods=['PUT'])
@authenticate
def reject(user, id):
    message = request.get_json()['message']

    try:
        publication = PublicationLogics().reject(id, message, user)
    except BadRequest as e:
        return failed_response(message=e.message, status_code=400)

    return success_response(
        data=publication,
        status_code=200)


@publications_blueprint.route(
    '/social/publications/<id>/accept', methods=['PUT'])
@authenticate
def accept(user, id):
    try:
        publication = PublicationLogics().accept(id, user)
    except BadRequest as e:
        return failed_response(message=e.message, status_code=400)

    return success_response(
        data=publication,
        status_code=200)


@publications_blueprint.route('/social/publications/<id>', methods=['DELETE'])
@authenticate
def delete(user, id):
    try:
        PublicationLogics().delete(id, user)
    except NotFound:
        return failed_response(message="not found", status_code=404)
    except BadRequest:
        return failed_response(message="bad status", status_code=400)

    return success_response(status_code=204)


@publications_blueprint.route('/social/publications/<id>', methods=['PUT'])
@authenticate
def update(user, id):
    publication_data = {}
    publication_data['date'] = request.form.get('date')
    publication_data['time'] = request.form.get('time')
    publication_data['title'] = request.form.get('title')
    publication_data['social_networks'] = request.form.get(
        'social_networks').split(',')
    publication_data['message'] = request.form.get('message')
    publication_data['additional'] = request.form.get('additional')
    publication_data['image'] = request.files.get('image')

    try:
        publication = PublicationLogics().update(id, publication_data, user)
    except NotFound:
        return failed_response(message="not found", status_code=404)
    except BadRequest as e:
        return failed_response(message=e.message, status_code=400)

    return success_response(
        data=publication,
        status_code=200)


@publications_blueprint.route(
    '/social/publications/<id>/link', methods=['PUT'])
@authenticate
def link(user, id):
    data = request.get_json()

    try:
        publication = PublicationLogics().link(id, data, user)
    except NotFound:
        return failed_response(message="not found", status_code=404)
    except BadRequest as e:
        return failed_response(message=e.message, status_code=400)

    return success_response(data=publication, status_code=200)
