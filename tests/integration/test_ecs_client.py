import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, EcsClient, Region, ServiceName
from aws_resource_validator.pydantic_models.ecs.ecs_classes import (
    CreateClusterRequestTypeDef,
    DescribeClustersRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_ecs_client(config):
    c = typed_boto3.client(ServiceName.ECS, config)
    assert isinstance(c, EcsClient)


@mock_aws
def test_create_and_describe_cluster(config):
    client = typed_boto3.client(ServiceName.ECS, config)
    client.create_cluster(CreateClusterRequestTypeDef(clusterName="my-cluster"))
    resp = client.describe_clusters(DescribeClustersRequestTypeDef(clusters=["my-cluster"]))
    assert resp is not None
    assert resp.clusters is not None
    assert len(resp.clusters) == 1
    assert resp.clusters[0].clusterName == "my-cluster"
