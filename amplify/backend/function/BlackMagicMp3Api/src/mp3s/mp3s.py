import json
import os
import time
from urllib.parse import unquote

import boto3
import constants
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import BadRequestError

S3_USER_MP3_BUCKET_NAME = os.environ["S3_USER_MP3_BUCKET_NAME"]

logger = Logger(child=True) 
router = Router()


@router.get("")
def delete_mp3():
    query_params = router.current_event.query_string_parameters
    logger.info(f"query_params is: {json.dumps(query_params)}")
    if not query_params:
        raise BadRequestError(
            f"{constants.MP3_TO_DELETE} is a required query parameter.")
    mp3_to_delete = unquote(query_params.get(constants.MP3_TO_DELETE))
    if not mp3_to_delete:
        raise BadRequestError(
            f"{constants.MP3_TO_DELETE} is a required query parameter.")
    logger.info(f"mp3_to_delete is: {json.dumps(mp3_to_delete)}")
    try:
        client = boto3.client("s3", region_name="us-east-1")
        time.sleep(360)
        logger.info(f"Removing mp3 with key {mp3_to_delete}.mp3")
        client.delete_object(Bucket=S3_USER_MP3_BUCKET_NAME, Key=f"{mp3_to_delete}.mp3")
        response = {
            'statusCode': 200,
            'body': f"{mp3_to_delete} has been deleted."
        }
        return response
    except OSError as err:
        logger.error(f"OS error: [ {err} ]")
    except BaseException as err:
        logger.error(f"BaseException error: [ {err} ]")
