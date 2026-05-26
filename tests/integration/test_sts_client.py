import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, Region, ServiceName, StsClient


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_sts_client(config):
    c = typed_boto3.client(ServiceName.STS, config)
    assert isinstance(c, StsClient)


@mock_aws
def test_get_caller_identity(config):
    client = typed_boto3.client(ServiceName.STS, config)
    resp = client.get_caller_identity()
    assert resp is not None
    assert resp.Account is not None
    assert resp.Arn is not None
