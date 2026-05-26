import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import Apigatewayv2Client, ClientConfig, Region, ServiceName
from aws_resource_validator.pydantic_models.apigatewayv2.apigatewayv2_classes import (
    CreateApiRequestTypeDef,
    GetApisRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_apigatewayv2_client(config):
    c = typed_boto3.client(ServiceName.APIGATEWAYV2, config)
    assert isinstance(c, Apigatewayv2Client)


@mock_aws
def test_create_and_list_apis(config):
    client = typed_boto3.client(ServiceName.APIGATEWAYV2, config)
    created = client.create_api(CreateApiRequestTypeDef(Name="my-http-api", ProtocolType="HTTP"))
    assert created is not None
    assert created.Name == "my-http-api"
    resp = client.get_apis(GetApisRequestTypeDef())
    assert resp is not None
    assert resp.Items is not None
    names = [a.Name for a in resp.Items]
    assert "my-http-api" in names
