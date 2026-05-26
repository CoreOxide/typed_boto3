import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ApigatewayClient, ClientConfig, Region, ServiceName
from aws_resource_validator.pydantic_models.apigateway.apigateway_classes import (
    CreateRestApiRequestTypeDef,
    GetRestApisRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_apigateway_client(config):
    c = typed_boto3.client(ServiceName.APIGATEWAY, config)
    assert isinstance(c, ApigatewayClient)


@mock_aws
def test_create_and_list_rest_apis(config):
    client = typed_boto3.client(ServiceName.APIGATEWAY, config)
    created = client.create_rest_api(CreateRestApiRequestTypeDef(name="my-api"))
    assert created is not None
    assert created.name == "my-api"
    resp = client.get_rest_apis(GetRestApisRequestTypeDef())
    assert resp is not None
    assert resp.items is not None
    names = [a.name for a in resp.items]
    assert "my-api" in names
