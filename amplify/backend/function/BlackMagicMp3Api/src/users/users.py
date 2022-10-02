import os
import json

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import (
    BadRequestError, NotFoundError)
from boto3.dynamodb.conditions import Key
from botocore import client


import constants

USERS_TABLE_NAME = os.environ["USERS_TABLE_NAME"]
S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

logger = Logger(child=True)
router = Router()
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(USERS_TABLE_NAME)


@router.get("/<user_email>")
def get_presigned_url(user_email: str) -> dict:
    query_params = router.current_event.query_string_parameters
    if not query_params:
        raise BadRequestError(f"{constants.BANDCAMP_CODE_QUERY_PARAM} is a required query parameter.")
    bandcamp_code = query_params.get(constants.BANDCAMP_CODE_QUERY_PARAM)
    if not bandcamp_code:
        raise BadRequestError(f"{constants.BANDCAMP_CODE_QUERY_PARAM} is a required query parameter.")
    logger.info(f"Fetching user with email [ {user_email} ]")
    response = table.query(
        KeyConditionExpression=Key("email").eq(user_email)
    )
    if constants.ITEMS not in response or not response[constants.ITEMS]:
        raise NotFoundError(
            f"[ {user_email} ] user email not found. Please try again with a valid email that was been verified with Black Magic.")
    user_id = response.get("Items")[0].get("id")
    presigned_url = build_presigned_url(user_id, bandcamp_code)
    return {
        "mp3Url": presigned_url,
        "mp3Name": bandcamp_code,
        "userId": user_id
    }


def build_presigned_url(user_id, bandcamp_code) -> str:
    s3 = boto3.client("s3", config=client.Config(signature_version="s3v4"))
    try:
        presigned_url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": S3_BUCKET_NAME,
                "Key": f"{user_id}/{bandcamp_code}.mp3"
            },
            ExpiresIn=300
        )
        return presigned_url
    except OSError as err:
        logger.error(f"OS error: [ {err} ]")
    except BaseException as err:
        logger.error(f"BaseException error: [ {err} ]")
