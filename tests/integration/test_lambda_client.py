import io
import json
import zipfile

import boto3
import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, LambdaClient, Region, ServiceName
from aws_resource_validator.pydantic_models.lambda_.lambda__classes import (
    CreateFunctionRequestTypeDef,
    FunctionCodeTypeDef,
    GetFunctionRequestTypeDef,
    ListFunctionsRequestTypeDef,
)


def _zip_bytes() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("lambda_function.py", "def lambda_handler(event, context):\n    return event\n")
    return buf.getvalue()


def _create_lambda_role() -> str:
    iam = boto3.client("iam", region_name="us-east-1")
    assume_role = {
        "Version": "2012-10-17",
        "Statement": [
            {"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}
        ],
    }
    role = iam.create_role(RoleName="lambda-role", AssumeRolePolicyDocument=json.dumps(assume_role))
    return role["Role"]["Arn"]


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_lambda_client(config):
    c = typed_boto3.client(ServiceName.LAMBDA, config)
    assert isinstance(c, LambdaClient)


@mock_aws
def test_create_and_get_function(config):
    role_arn = _create_lambda_role()
    client = typed_boto3.client(ServiceName.LAMBDA, config)

    created = client.create_function(
        CreateFunctionRequestTypeDef(
            FunctionName="my-fn",
            Runtime="python3.11",
            Role=role_arn,
            Handler="lambda_function.lambda_handler",
            Code=FunctionCodeTypeDef(ZipFile=_zip_bytes()),
        )
    )
    assert created is not None
    assert created.FunctionName == "my-fn"
    assert created.Runtime == "python3.11"

    fetched = client.get_function(GetFunctionRequestTypeDef(FunctionName="my-fn"))
    assert fetched is not None
    assert fetched.Configuration is not None
    assert fetched.Configuration.FunctionName == "my-fn"


@mock_aws
def test_list_functions_empty(config):
    client = typed_boto3.client(ServiceName.LAMBDA, config)
    resp = client.list_functions(ListFunctionsRequestTypeDef())
    assert resp is not None
    assert not resp.Functions


@mock_aws
def test_direct_client_class(config):
    client = LambdaClient(config)
    resp = client.list_functions(ListFunctionsRequestTypeDef())
    assert resp is not None
