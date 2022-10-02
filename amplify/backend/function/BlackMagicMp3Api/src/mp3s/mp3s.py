import os
import time

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import BadRequestError

import constants

S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

logger = Logger(child=True)
router = Router()
dynamodb = boto3.resource("dynamodb")


@router.delete("/<mp3_name>")
def delete_mp3(mp3_name: str) -> dict:
    query_params = router.current_event.query_string_parameters
    if not query_params:
        raise BadRequestError(
            f"{constants.USER_ID_QUERY_PARAM} is a required query parameter.")
    user_id = query_params.get(constants.USER_ID_QUERY_PARAM)
    if not user_id:
        raise BadRequestError(
            f"{constants.USER_ID_QUERY_PARAM} is a required query parameter.")
    try:
        client = boto3.client('s3')
        time.sleep(360)
        logger.info(f"Removing mp3 with key {user_id}/{mp3_name}.mp3")
        client.delete_object(Bucket=S3_BUCKET_NAME, Key=f"{user_id}/{mp3_name}.mp3")
    except OSError as err:
        logger.error(f"OS error: [ {err} ]")
    except BaseException as err:
        logger.error(f"BaseException error: [ {err} ]")
