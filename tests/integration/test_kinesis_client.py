import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, KinesisClient, Region, ServiceName
from aws_resource_validator.pydantic_models.kinesis.kinesis_classes import (
    CreateStreamInputTypeDef,
    DescribeStreamInputTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_kinesis_client(config):
    c = typed_boto3.client(ServiceName.KINESIS, config)
    assert isinstance(c, KinesisClient)


@mock_aws
def test_create_and_describe_stream(config):
    client = typed_boto3.client(ServiceName.KINESIS, config)
    client.create_stream(CreateStreamInputTypeDef(StreamName="my-stream", ShardCount=1))
    resp = client.describe_stream(DescribeStreamInputTypeDef(StreamName="my-stream"))
    assert resp is not None
    assert resp.StreamDescription is not None
    assert resp.StreamDescription.StreamName == "my-stream"
