from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = ""
    bucket_name = 'riotapi-media'
    region_name = 'us-west-1'
    custom_domain = f"s3.{region_name}.amazonaws.com/{bucket_name}"
    file_overwrite = False
