import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, Region, ServiceName, SsmClient
from aws_resource_validator.pydantic_models.ssm.ssm_classes import (
    GetParameterRequestTypeDef,
    PutParameterRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_ssm_client(config):
    c = typed_boto3.client(ServiceName.SSM, config)
    assert isinstance(c, SsmClient)


@mock_aws
def test_put_and_get_parameter(config):
    client = typed_boto3.client(ServiceName.SSM, config)
    client.put_parameter(
        PutParameterRequestTypeDef(Name="/my/param", Value="hello", Type="String")
    )
    resp = client.get_parameter(GetParameterRequestTypeDef(Name="/my/param"))
    assert resp is not None
    assert resp.Parameter is not None
    assert resp.Parameter.Value == "hello"
