import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, KmsClient, Region, ServiceName
from aws_resource_validator.pydantic_models.kms.kms_classes import (
    CreateKeyRequestTypeDef,
    DescribeKeyRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_kms_client(config):
    c = typed_boto3.client(ServiceName.KMS, config)
    assert isinstance(c, KmsClient)


@mock_aws
def test_create_and_describe_key(config):
    client = typed_boto3.client(ServiceName.KMS, config)
    created = client.create_key(CreateKeyRequestTypeDef(Description="test-key"))
    assert created is not None
    assert created.KeyMetadata is not None
    key_id = created.KeyMetadata.KeyId
    resp = client.describe_key(DescribeKeyRequestTypeDef(KeyId=key_id))
    assert resp is not None
    assert resp.KeyMetadata is not None
    assert resp.KeyMetadata.KeyId == key_id
