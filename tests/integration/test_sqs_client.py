import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, Region, ServiceName, SqsClient
from aws_resource_validator.pydantic_models.sqs.sqs_classes import (
    CreateQueueRequestTypeDef,
    ListQueuesRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_sqs_client(config):
    c = typed_boto3.client(ServiceName.SQS, config)
    assert isinstance(c, SqsClient)


@mock_aws
def test_create_and_list_queues(config):
    client = typed_boto3.client(ServiceName.SQS, config)
    created = client.create_queue(CreateQueueRequestTypeDef(QueueName="my-queue"))
    assert created is not None
    assert created.QueueUrl is not None
    resp = client.list_queues(ListQueuesRequestTypeDef())
    assert resp is not None
    assert resp.QueueUrls is not None
    assert created.QueueUrl in resp.QueueUrls
