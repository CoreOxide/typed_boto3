import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, EventsClient, Region, ServiceName
from aws_resource_validator.pydantic_models.events.events_classes import (
    ListRulesRequestTypeDef,
    PutRuleRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_events_client(config):
    c = typed_boto3.client(ServiceName.EVENTS, config)
    assert isinstance(c, EventsClient)


@mock_aws
def test_put_and_list_rules(config):
    client = typed_boto3.client(ServiceName.EVENTS, config)
    client.put_rule(PutRuleRequestTypeDef(Name="my-rule", ScheduleExpression="rate(5 minutes)"))
    resp = client.list_rules(ListRulesRequestTypeDef(NamePrefix="my-rule"))
    assert resp is not None
    assert resp.Rules is not None
    names = [r.Name for r in resp.Rules]
    assert "my-rule" in names
