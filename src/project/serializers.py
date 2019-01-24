class PublicationSerializer:
    @staticmethod
    def to_dict(publication):
        return {
            'id': publication.id,
            'company_id': publication.company_id,
            'company_identifier': publication.company['identifier'],
            'company_name': publication.company['name'],
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
                publication),
            'link': publication.link,
            'tags': PublicationSerializer.__tags(publication)
        }

    @staticmethod
    def to_array(publications):
        return list(
            map(
                lambda publication: PublicationSerializer.to_dict(publication),
                publications))

    @staticmethod
    def __social_networks(publication):
        return list(map(
            lambda network: network.social_network,
            publication.social_networks))

    @staticmethod
    def __tags(publication):
        return list(map(lambda tag: tag.name, publication.tags))


class CategorySerializer:
    @staticmethod
    def to_dict(category):
        return {
            'id': category.id,
            'name': category.name,
            'subcategories': SubcategorySerializer.to_array(
                category.subcategories)
        }

    @staticmethod
    def to_array(categories):
        return list(
            map(
                lambda category: CategorySerializer.to_dict(category),
                categories))


class SubcategorySerializer:
    @staticmethod
    def to_dict(subcategory):
        return {
            'id': subcategory.id,
            'name': subcategory.name,
            'company_id': subcategory.company_id
        }

    @staticmethod
    def to_array(subcategories):
        return list(
            map(
                lambda subcategory: SubcategorySerializer.to_dict(subcategory),
                subcategories))
