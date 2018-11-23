from project import db
from sqlalchemy.sql import func


class FacebookAuth(db.Model):
    __tablename__ = 'facebook_auth'
    __table_args__ = {'schema': 'social'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=func.now(), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)

    code = db.Column(db.String(2048), nullable=True)
    code_created = db.Column(db.DateTime, nullable=True)

    short_lived_access_token = db.Column(db.String(128), nullable=True)
    short_lived_access_token_created = db.Column(db.DateTime, nullable=True)
