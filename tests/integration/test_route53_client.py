import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, Region, Route53Client, ServiceName
from aws_resource_validator.pydantic_models.route53.route53_classes import (
    CreateHostedZoneRequestTypeDef,
    GetHostedZoneRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_route53_client(config):
    c = typed_boto3.client(ServiceName.ROUTE53, config)
    assert isinstance(c, Route53Client)


@mock_aws
def test_create_and_get_hosted_zone(config):
    client = typed_boto3.client(ServiceName.ROUTE53, config)
    created = client.create_hosted_zone(
        CreateHostedZoneRequestTypeDef(Name="example.com.", CallerReference="ref-1")
    )
    assert created is not None
    assert created.HostedZone is not None
    zone_id = created.HostedZone.Id
    assert zone_id is not None
    resp = client.get_hosted_zone(GetHostedZoneRequestTypeDef(Id=zone_id))
    assert resp is not None
    assert resp.HostedZone is not None
    assert resp.HostedZone.Id == zone_id
