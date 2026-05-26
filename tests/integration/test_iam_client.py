import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, IamClient, Region, ServiceName
from aws_resource_validator.pydantic_models.iam.iam_classes import (
    CreateUserRequestTypeDef,
    GetUserRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_iam_client(config):
    c = typed_boto3.client(ServiceName.IAM, config)
    assert isinstance(c, IamClient)


@mock_aws
def test_create_and_get_user(config):
    client = typed_boto3.client(ServiceName.IAM, config)
    client.create_user(CreateUserRequestTypeDef(UserName="alice"))
    resp = client.get_user(GetUserRequestTypeDef(UserName="alice"))
    assert resp is not None
    assert resp.User is not None
    assert resp.User.UserName == "alice"
