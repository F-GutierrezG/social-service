import enum

from project import db
from sqlalchemy.sql import func


class Publication(db.Model):
    __tablename__ = 'publications'
    __table_args__ = {'schema': 'social'}

    class Status(enum.Enum):
        PENDING = 'PENDING'
        ACCEPTED = 'ACCEPTED'
        REJECTED = 'REJECTED'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=func.now(), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)

    updated = db.Column(db.DateTime, onupdate=func.now())
    updated_by = db.Column(db.Integer)

    datetime = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(32), db.Enum(Status), default=Status.PENDING, nullable=False)

    social_networks = db.relationship(
        "PublicationSocialNetwork", backref='publication')


class PublicationSocialNetwork(db.Model):
    __tablename__ = 'publication_social_networks'
    __table_args__ = {'schema': 'social'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    social_network = db.Column(db.String(128), nullable=False)
    publication_id = db.Column(
        db.Integer,
        db.ForeignKey(Publication.id),
        nullable=False)


class FacebookAuth(db.Model):
    __tablename__ = 'facebook_auth'
    __table_args__ = {'schema': 'social'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=func.now(), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)

    code = db.Column(db.String(2048), nullable=True)
    code_created = db.Column(db.DateTime, nullable=True)

    short_lived_access_token = db.Column(db.String(256), nullable=True)
    short_lived_access_token_created = db.Column(db.DateTime, nullable=True)
