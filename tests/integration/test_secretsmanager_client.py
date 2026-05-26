import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, Region, SecretsmanagerClient, ServiceName
from aws_resource_validator.pydantic_models.secretsmanager.secretsmanager_classes import (
    CreateSecretRequestTypeDef,
    DescribeSecretRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_secretsmanager_client(config):
    c = typed_boto3.client(ServiceName.SECRETSMANAGER, config)
    assert isinstance(c, SecretsmanagerClient)


@mock_aws
def test_create_and_describe_secret(config):
    client = typed_boto3.client(ServiceName.SECRETSMANAGER, config)
    client.create_secret(
        CreateSecretRequestTypeDef(Name="my-secret", SecretString="hunter2")
    )
    resp = client.describe_secret(DescribeSecretRequestTypeDef(SecretId="my-secret"))
    assert resp is not None
    assert resp.Name == "my-secret"
