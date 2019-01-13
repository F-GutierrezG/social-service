import uuid
import boto3

from flask import current_app


class S3Uploader:
    def upload(self, file):
        bucket_name = current_app.config['AWS_BUCKET_NAME']
        key = 'images/{}'.format(self.__generate_name(file))

        s3 = boto3.resource('s3')
        s3.Bucket(bucket_name).put_object(
            Key=key,
            Body=file,
            ContentType=file.mimetype)

        return "https://s3.amazonaws.com/{}/{}".format(
            bucket_name, key)

    def __generate_name(self, file):
        extension = file.filename.split('.')[-1]

        return '{}.{}'.format(uuid.uuid4().hex, extension)
