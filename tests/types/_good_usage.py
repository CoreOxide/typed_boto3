"""Must type-check under mypy --strict."""
from typing import assert_type

import typed_boto3
from typed_boto3 import ClientConfig, LambdaClient, Region, S3Client, ServiceName
from aws_resource_validator.pydantic_models.lambda_.lambda__classes import (
    CreateFunctionRequestTypeDef,
    FunctionCodeTypeDef,
    FunctionConfigurationTypeDef,
)


def good_factory() -> None:
    config = ClientConfig(region=Region.US_EAST_1)
    c = typed_boto3.client(ServiceName.LAMBDA, config)
    assert_type(c, LambdaClient)

    s = typed_boto3.client(ServiceName.S3, config)
    assert_type(s, S3Client)


def good_direct() -> None:
    c = LambdaClient(ClientConfig(region=Region.US_EAST_1))
    resp = c.create_function(
        CreateFunctionRequestTypeDef(
            FunctionName="fn",
            Runtime="python3.11",
            Role="arn:aws:iam::123456789012:role/r",
            Handler="x.y",
            Code=FunctionCodeTypeDef(ZipFile=b"..."),
        )
    )
    assert_type(resp, FunctionConfigurationTypeDef)
