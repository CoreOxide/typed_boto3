import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, Region, ServiceName, SnsClient
from aws_resource_validator.pydantic_models.sns.sns_classes import (
    CreateTopicInputTypeDef,
    ListTopicsInputTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_sns_client(config):
    c = typed_boto3.client(ServiceName.SNS, config)
    assert isinstance(c, SnsClient)


@mock_aws
def test_create_and_list_topics(config):
    client = typed_boto3.client(ServiceName.SNS, config)
    created = client.create_topic(CreateTopicInputTypeDef(Name="my-topic"))
    assert created is not None
    assert created.TopicArn is not None
    resp = client.list_topics(ListTopicsInputTypeDef())
    assert resp is not None
    assert resp.Topics is not None
    arns = [t.TopicArn for t in resp.Topics]
    assert created.TopicArn in arns
