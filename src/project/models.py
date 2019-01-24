import enum

from companies_service.factories import CompaniesServiceFactory

from project import db
from sqlalchemy.sql import func


class Publication(db.Model):
    __tablename__ = 'publications'
    __table_args__ = {'schema': 'social'}

    class Status(enum.Enum):
        PENDING = 'PENDING'
        ACCEPTED = 'ACCEPTED'
        REJECTED = 'REJECTED'
        DELETED = 'DELETED'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=func.now(), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)

    updated = db.Column(db.DateTime, onupdate=func.now())
    updated_by = db.Column(db.Integer)

    datetime = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=True)
    additional = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.Enum(Status),
        default=Status.PENDING,
        nullable=False)
    reject_reason = db.Column(db.Text, nullable=True)
    link = db.Column(db.Text, nullable=True)
    parent_id = db.Column(db.Integer, nullable=True)

    social_networks = db.relationship(
        "PublicationSocialNetwork", backref='publication')
    tags = db.relationship("PublicationTag", backref='publication')

    _company = None

    @property
    def company(self):
        if self._company is None:
            service = CompaniesServiceFactory.get_instance()
            _, self._company = service.get_company(self.company_id)

        return self._company


class PublicationSocialNetwork(db.Model):
    __tablename__ = 'publication_social_networks'
    __table_args__ = {'schema': 'social'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    social_network = db.Column(db.String(128), nullable=False)
    publication_id = db.Column(
        db.Integer,
        db.ForeignKey(Publication.id),
        nullable=False)


class PublicationTag(db.Model):
    __tablename__ = 'publication_tags'
    __table_args__ = {'schema': 'social'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    publication_id = db.Column(
        db.Integer,
        db.ForeignKey(Publication.id),
        nullable=False)


class Category(db.Model):
    __tablename__ = 'categories'
    __table_args__ = {'schema': 'social'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    subcategories = db.relationship(
        "Subcategory", backref='category')


class Subcategory(db.Model):
    __tablename__ = 'subcategories'
    __table_args__ = {'schema': 'social'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(512), nullable=False)
    company_id = db.Column(db.Integer)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey(Category.id),
        nullable=False)
