import os

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import (
    BadRequestError, InternalServerError, NotFoundError)
from boto3.dynamodb.conditions import Key


import constants

CODES_TABLE_NAME = os.environ["CODES_TABLE_NAME"]
USERS_TABLE_NAME = os.environ["USERS_TABLE_NAME"]
S3_MP3_SOURCE_BUCKET_NAME = os.environ["S3_MP3_SOURCE_BUCKET_NAME"]
S3_USER_MP3_BUCKET_NAME = os.environ["S3_USER_MP3_BUCKET_NAME"]

logger = Logger(child=True)
router = Router()
dynamodb = boto3.resource("dynamodb")
s3 = boto3.resource("s3")
codes_table = dynamodb.Table(CODES_TABLE_NAME)
users_table = dynamodb.Table(USERS_TABLE_NAME)


@router.get("/<user_email>")
def get_presigned_url(user_email: str) -> dict:
    query_params = router.current_event.query_string_parameters
    if not query_params:
        raise BadRequestError(f"{constants.BANDCAMP_CODE_QUERY_PARAM} is a required query parameter.")
    bandcamp_code = query_params.get(constants.BANDCAMP_CODE_QUERY_PARAM)
    if not bandcamp_code:
        raise BadRequestError(f"{constants.BANDCAMP_CODE_QUERY_PARAM} is a required query parameter.")
    user_query_response = query_user_email(user_email)
    validate_user_query_response(user_query_response, user_email, bandcamp_code)
    user_id = user_query_response.get("Items")[0].get("id")
    add_mp3_for_user(bandcamp_code, user_id)
    record_mp3_downloaded(user_query_response.get("Items")[0], bandcamp_code)
    presigned_url = build_presigned_url(user_id, bandcamp_code)
    return {
        "mp3Url": presigned_url,
        "mp3Name": bandcamp_code,
        "userId": user_id
    }

def query_user_email(user_email: str) -> dict:
    logger.info(f"Fetching user with email [ {user_email} ]")
    return users_table.query(
        KeyConditionExpression=Key("email").eq(user_email)
    )

def validate_user_query_response(user_query_response: dict, user_email: str, bandcamp_code: str):
    if constants.ITEMS not in user_query_response or not user_query_response[constants.ITEMS]:
        raise NotFoundError(
            f"[ {user_email} ] user email not found. Please try again with a valid email that was been verified with Black Magic.")
    if (user_query_response.get("Items")[0].get("downloads", {}).get(bandcamp_code)):
        raise InternalServerError(f"User with email [ {user_email} ] has already downloaded [ {bandcamp_code}.mp3 ]")
    validate_bandcamp_code(bandcamp_code)

def validate_bandcamp_code(bandcamp_code: str):
    code_query_response = codes_table.query(
        KeyConditionExpression=Key('code').eq(bandcamp_code)
    )
    if constants.ITEMS not in code_query_response or not code_query_response[constants.ITEMS]:
        raise NotFoundError(f"[ {bandcamp_code} ] code not found. Please try again with a valid code from a Bandcamp release PDF.")

def add_mp3_for_user(bandcamp_code: str, user_id: str):
    copy_source = {
      "Bucket": S3_MP3_SOURCE_BUCKET_NAME,
      "Key": f"{bandcamp_code}.mp3"
    }
    user_mp3_bucket = s3.Bucket(S3_USER_MP3_BUCKET_NAME)
    user_mp3_bucket.copy(copy_source, f"{user_id}/{bandcamp_code}.mp3")

def record_mp3_downloaded(user_item: dict, bandcamp_code: str):
    if ("downloads" not in user_item or not user_item["downloads"]):
        user_item["downloads"] = { bandcamp_code: 'downloaded'}
    else:
        user_item["downloads"][bandcamp_code] = 'downloaded'
    users_table.put_item(Item=user_item)

def build_presigned_url(user_id: str, bandcamp_code: str) -> str:
    s3_client = boto3.client("s3", region_name="us-east-1", config=boto3.session.Config(signature_version="s3v4"))
    try:
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": S3_USER_MP3_BUCKET_NAME,
                "Key": f"{user_id}/{bandcamp_code}.mp3"
            },
            ExpiresIn=360
        )

        return presigned_url
    except OSError as err:
        logger.error(f"OS error: [ {err} ]")
    except BaseException as err:
        logger.error(f"BaseException error: [ {err} ]")
