import pandas as pd
import boto3
import os
from dotenv import load_dotenv
from io import StringIO

load_dotenv()

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    region_name=os.getenv("REGION_NAME")
)


def create_dataframe_from_s3(bucket: str, key: str) -> pd.DataFrame:
    """
    Return a dataframe from a csv stored in AWS S3.
    Parameters
    ----------
    bucket: Bucket name.
    key: The file name

    Returns
    -------
    A pandas dataframe from a csv.
    """
    obj = s3.get_object(Bucket=bucket, Key=key)
    body = obj['Body']
    csv_string = body.read().decode('utf-8')

    dataframe = pd.read_csv(StringIO(csv_string))
    return dataframe
