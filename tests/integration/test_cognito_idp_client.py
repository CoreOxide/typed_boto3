import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, CognitoIdpClient, Region, ServiceName
from aws_resource_validator.pydantic_models.cognito_idp.cognito_idp_classes import (
    CreateUserPoolRequestTypeDef,
    DescribeUserPoolRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_cognito_idp_client(config):
    c = typed_boto3.client(ServiceName.COGNITO_IDP, config)
    assert isinstance(c, CognitoIdpClient)


@mock_aws
def test_create_and_describe_user_pool(config):
    client = typed_boto3.client(ServiceName.COGNITO_IDP, config)
    created = client.create_user_pool(CreateUserPoolRequestTypeDef(PoolName="my-pool"))
    assert created is not None
    assert created.UserPool is not None
    pool_id = created.UserPool.Id
    assert pool_id is not None
    resp = client.describe_user_pool(DescribeUserPoolRequestTypeDef(UserPoolId=pool_id))
    assert resp is not None
    assert resp.UserPool is not None
    assert resp.UserPool.Id == pool_id
