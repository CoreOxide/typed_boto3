import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, RedshiftClient, Region, ServiceName
from aws_resource_validator.pydantic_models.redshift.redshift_classes import (
    CreateClusterMessageTypeDef,
    DescribeClustersMessageTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_redshift_client(config):
    c = typed_boto3.client(ServiceName.REDSHIFT, config)
    assert isinstance(c, RedshiftClient)


@mock_aws
def test_create_and_describe_cluster(config):
    client = typed_boto3.client(ServiceName.REDSHIFT, config)
    client.create_cluster(
        CreateClusterMessageTypeDef(
            ClusterIdentifier="my-cluster",
            NodeType="dc2.large",
            MasterUsername="admin",
            MasterUserPassword="hunter2hunter2A",
            ClusterType="single-node",
        )
    )
    resp = client.describe_clusters(
        DescribeClustersMessageTypeDef(ClusterIdentifier="my-cluster")
    )
    assert resp is not None
    assert resp.Clusters is not None
    assert len(resp.Clusters) == 1
    assert resp.Clusters[0].ClusterIdentifier == "my-cluster"
