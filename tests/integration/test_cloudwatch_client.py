import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, CloudwatchClient, Region, ServiceName
from aws_resource_validator.pydantic_models.cloudwatch.cloudwatch_classes import (
    DescribeAlarmsInputTypeDef,
    PutMetricAlarmInputTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_cloudwatch_client(config):
    c = typed_boto3.client(ServiceName.CLOUDWATCH, config)
    assert isinstance(c, CloudwatchClient)


@mock_aws
def test_put_and_describe_alarm(config):
    client = typed_boto3.client(ServiceName.CLOUDWATCH, config)
    client.put_metric_alarm(
        PutMetricAlarmInputTypeDef(
            AlarmName="cpu-high",
            MetricName="CPUUtilization",
            Namespace="AWS/EC2",
            Statistic="Average",
            Period=60,
            EvaluationPeriods=1,
            Threshold=80.0,
            ComparisonOperator="GreaterThanThreshold",
        )
    )
    resp = client.describe_alarms(DescribeAlarmsInputTypeDef(AlarmNames=["cpu-high"]))
    assert resp is not None
    assert resp.MetricAlarms is not None
    assert len(resp.MetricAlarms) == 1
    assert resp.MetricAlarms[0].AlarmName == "cpu-high"
