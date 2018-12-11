class PublicationSerializer:
    @staticmethod
    def to_dict(publication):
        return {
            'id': publication.id,
            'company_id': publication.company_id,
            'datetime': publication.datetime,
            'message': publication.message,
            'image_url': publication.image_url,
            'created': str(publication.created),
            'created_by': publication.created_by,
            'updated': str(publication.updated),
            'updated_by': publication.updated_by,
        }
