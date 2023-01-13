import boto3
from pprint import pprint
import pathlib
import os

ACCESS_KEY="AKIAY74ITD5OHT7ILGBN"
SECRET_KEY="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"

s3 = boto3.client("s3", 
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY)

def upload_file_using_client():
    """
    Uploads file to S3 bucket using S3 client object
    :return: None
    """
    bucket_name = "ntaweli-hr"
    object_name = "bernard.png"
    file_name = os.path.join(pathlib.Path(__file__).parent.resolve(), "mycontact.png")

    response = s3.upload_file(file_name, bucket_name, object_name)
    a = s3.download_file('ntaweli-hr', 'bernard.png', 'test.png')
    print(a)
    pprint(response)  # prints None

upload_file_using_client()