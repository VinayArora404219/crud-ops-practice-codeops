
import boto3


def get_s3_client(profile_name='default', region_name=None):
    session = boto3.session.Session(
        profile_name=profile_name,
        region_name=region_name
    )
    s3 = session.client('s3')

    return s3


def get_sns_client(profile_name='default', region_name='ap-south-1'):
    session = boto3.session.Session(
        profile_name=profile_name,
        region_name=region_name
    )
    sns = session.client('sns')

    return sns
