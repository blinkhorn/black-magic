from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, CORSConfig
from aws_lambda_powertools.utilities.typing import LambdaContext

import mp3s.mp3s as mp3s
import users.users as users
import codes.codes as codes

logger = Logger()
cors_config = CORSConfig(allow_origin="https://prod.d2en0760w44xya.amplifyapp.com", allow_credentials=True)
app = ApiGatewayResolver(cors=cors_config)

app.include_router(mp3s.router, prefix="/api/mp3s")
app.include_router(users.router, prefix="/api/users")
app.include_router(codes.router, prefix="/api/codes")


def handler(event: dict, context: LambdaContext):
    return app.resolve(event, context)