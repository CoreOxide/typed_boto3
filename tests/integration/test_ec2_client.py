import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, Ec2Client, Region, ServiceName
from aws_resource_validator.pydantic_models.ec2.ec2_classes import (
    DescribeInstancesRequestTypeDef,
    DescribeRegionsRequestTypeDef,
    RunInstancesRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_ec2_client(config):
    c = typed_boto3.client(ServiceName.EC2, config)
    assert isinstance(c, Ec2Client)


@mock_aws
def test_describe_regions_returns_typed_response(config):
    client = Ec2Client(config)
    resp = client.describe_regions(DescribeRegionsRequestTypeDef())
    assert resp is not None
    assert resp.Regions is not None
    assert len(resp.Regions) > 0


@mock_aws
def test_run_and_describe_instances(config):
    client = typed_boto3.client(ServiceName.EC2, config)
    client.run_instances(
        RunInstancesRequestTypeDef(
            ImageId="ami-12345678",
            InstanceType="t2.micro",
            MinCount=1,
            MaxCount=1,
        )
    )
    resp = client.describe_instances(DescribeInstancesRequestTypeDef())
    assert resp is not None
    assert resp.Reservations is not None
    assert len(resp.Reservations) == 1
    assert resp.Reservations[0].Instances is not None
    assert len(resp.Reservations[0].Instances) == 1
