import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, FirehoseClient, Region, ServiceName
from aws_resource_validator.pydantic_models.firehose.firehose_classes import (
    CreateDeliveryStreamInputTypeDef,
    DescribeDeliveryStreamInputTypeDef,
    ExtendedS3DestinationConfigurationTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_firehose_client(config):
    c = typed_boto3.client(ServiceName.FIREHOSE, config)
    assert isinstance(c, FirehoseClient)


@mock_aws
def test_create_and_describe_delivery_stream(config):
    client = typed_boto3.client(ServiceName.FIREHOSE, config)
    client.create_delivery_stream(
        CreateDeliveryStreamInputTypeDef(
            DeliveryStreamName="my-stream",
            ExtendedS3DestinationConfiguration=ExtendedS3DestinationConfigurationTypeDef(
                RoleARN="arn:aws:iam::123456789012:role/firehose-role",
                BucketARN="arn:aws:s3:::my-bucket",
            ),
        )
    )
    resp = client.describe_delivery_stream(
        DescribeDeliveryStreamInputTypeDef(DeliveryStreamName="my-stream")
    )
    assert resp is not None
    assert resp.DeliveryStreamDescription is not None
    assert resp.DeliveryStreamDescription.DeliveryStreamName == "my-stream"
