import boto3
import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, Elbv2Client, Region, ServiceName
from aws_resource_validator.pydantic_models.elbv2.elbv2_classes import (
    CreateLoadBalancerInputTypeDef,
    DescribeLoadBalancersInputTypeDef,
)


def _create_subnets() -> list[str]:
    ec2 = boto3.client("ec2", region_name="us-east-1")
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")["Vpc"]["VpcId"]
    subnet_a = ec2.create_subnet(VpcId=vpc, CidrBlock="10.0.1.0/24", AvailabilityZone="us-east-1a")[
        "Subnet"
    ]["SubnetId"]
    subnet_b = ec2.create_subnet(VpcId=vpc, CidrBlock="10.0.2.0/24", AvailabilityZone="us-east-1b")[
        "Subnet"
    ]["SubnetId"]
    return [subnet_a, subnet_b]


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_elbv2_client(config):
    c = typed_boto3.client(ServiceName.ELBV2, config)
    assert isinstance(c, Elbv2Client)


@mock_aws
def test_create_and_describe_load_balancer(config):
    subnets = _create_subnets()
    client = typed_boto3.client(ServiceName.ELBV2, config)
    client.create_load_balancer(
        CreateLoadBalancerInputTypeDef(Name="my-lb", Subnets=subnets, Scheme="internet-facing", Type="application")
    )
    resp = client.describe_load_balancers(DescribeLoadBalancersInputTypeDef(Names=["my-lb"]))
    assert resp is not None
    assert resp.LoadBalancers is not None
    assert len(resp.LoadBalancers) == 1
    assert resp.LoadBalancers[0].LoadBalancerName == "my-lb"
