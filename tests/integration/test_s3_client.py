import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, Region, S3Client, ServiceName
from aws_resource_validator.pydantic_models.s3.s3_classes import (
    CreateBucketRequestTypeDef,
    ListBucketsRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_s3_client(config):
    c = typed_boto3.client(ServiceName.S3, config)
    assert isinstance(c, S3Client)


@mock_aws
def test_create_and_list_buckets(config):
    client = typed_boto3.client(ServiceName.S3, config)

    client.create_bucket(CreateBucketRequestTypeDef(Bucket="my-bucket"))
    resp = client.list_buckets(ListBucketsRequestTypeDef())
    assert resp is not None
    assert resp.Buckets is not None
    names = [b.Name for b in resp.Buckets]
    assert "my-bucket" in names
