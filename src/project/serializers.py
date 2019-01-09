class PublicationSerializer:
    @staticmethod
    def to_dict(publication):
        return {
            'id': publication.id,
            'company_id': publication.company_id,
            'date': publication.datetime.strftime('%Y-%m-%d'),
            'time': publication.datetime.strftime('%H:%M'),
            'title': publication.title,
            'message': publication.message,
            'additional': publication.additional,
            'image_url': publication.image_url,
            'created': str(publication.created),
            'created_by': publication.created_by,
            'updated': str(publication.updated),
            'updated_by': publication.updated_by,
            'status': publication.status.value,
            'social_networks': PublicationSerializer.__social_networks(
                publication)
        }

    @staticmethod
    def to_array(publications):
        publications_list = []

        for publication in publications:
            publications_list.append(
                PublicationSerializer.to_dict(publication))

        return publications_list

    @staticmethod
    def __social_networks(publication):
        social_networks = []

        for network in publication.social_networks:
            social_networks.append(network.social_network)

        return social_networks
