import json

import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, CloudformationClient, Region, ServiceName
from aws_resource_validator.pydantic_models.cloudformation.cloudformation_classes import (
    CreateStackInputTypeDef,
    DescribeStacksInputTypeDef,
)


_EMPTY_TEMPLATE = json.dumps(
    {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Resources": {
            "Bucket": {"Type": "AWS::S3::Bucket"},
        },
    }
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_cloudformation_client(config):
    c = typed_boto3.client(ServiceName.CLOUDFORMATION, config)
    assert isinstance(c, CloudformationClient)


@mock_aws
def test_create_and_describe_stack(config):
    client = typed_boto3.client(ServiceName.CLOUDFORMATION, config)
    client.create_stack(
        CreateStackInputTypeDef(StackName="my-stack", TemplateBody=_EMPTY_TEMPLATE)
    )
    resp = client.describe_stacks(DescribeStacksInputTypeDef(StackName="my-stack"))
    assert resp is not None
    assert resp.Stacks is not None
    assert len(resp.Stacks) == 1
    assert resp.Stacks[0].StackName == "my-stack"
