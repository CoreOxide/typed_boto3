import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, LogsClient, Region, ServiceName
from aws_resource_validator.pydantic_models.logs.logs_classes import (
    CreateLogGroupRequestTypeDef,
    DescribeLogGroupsRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_logs_client(config):
    c = typed_boto3.client(ServiceName.LOGS, config)
    assert isinstance(c, LogsClient)


@mock_aws
def test_create_and_describe_log_group(config):
    client = typed_boto3.client(ServiceName.LOGS, config)
    client.create_log_group(CreateLogGroupRequestTypeDef(logGroupName="my-group"))
    resp = client.describe_log_groups(DescribeLogGroupsRequestTypeDef(logGroupNamePrefix="my-group"))
    assert resp is not None
    assert resp.logGroups is not None
    names = [g.logGroupName for g in resp.logGroups]
    assert "my-group" in names
