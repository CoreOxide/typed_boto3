import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, Region, SagemakerClient, ServiceName
from aws_resource_validator.pydantic_models.sagemaker.sagemaker_classes import (
    ContainerDefinitionTypeDef,
    CreateModelInputTypeDef,
    DescribeModelInputTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_sagemaker_client(config):
    c = typed_boto3.client(ServiceName.SAGEMAKER, config)
    assert isinstance(c, SagemakerClient)


@mock_aws
def test_create_and_describe_model(config):
    client = typed_boto3.client(ServiceName.SAGEMAKER, config)
    client.create_model(
        CreateModelInputTypeDef(
            ModelName="my-model",
            PrimaryContainer=ContainerDefinitionTypeDef(
                Image="123456789012.dkr.ecr.us-east-1.amazonaws.com/my-image:latest"
            ),
            ExecutionRoleArn="arn:aws:iam::123456789012:role/sm-role",
        )
    )
    resp = client.describe_model(DescribeModelInputTypeDef(ModelName="my-model"))
    assert resp is not None
    assert resp.ModelName == "my-model"
