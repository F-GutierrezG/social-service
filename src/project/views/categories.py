from flask import Blueprint

from auth.decorators import authenticate
from project.logics import CategoryLogics
from project.views.utils import success_response


categories_blueprint = Blueprint('categories', __name__)


@categories_blueprint.route('/social/categories/<id>', methods=['GET'])
@authenticate
def list(user, id):
    categories = CategoryLogics().list(id)

    return success_response(
        data=categories,
        status_code=200)
