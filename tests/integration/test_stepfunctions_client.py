import json

import boto3
import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, Region, ServiceName, StepfunctionsClient
from aws_resource_validator.pydantic_models.stepfunctions.stepfunctions_classes import (
    CreateStateMachineInputTypeDef,
    DescribeStateMachineInputTypeDef,
)


def _create_role() -> str:
    iam = boto3.client("iam", region_name="us-east-1")
    role = iam.create_role(
        RoleName="sfn-role",
        AssumeRolePolicyDocument=json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"Service": "states.amazonaws.com"},
                        "Action": "sts:AssumeRole",
                    }
                ],
            }
        ),
    )
    return role["Role"]["Arn"]


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_stepfunctions_client(config):
    c = typed_boto3.client(ServiceName.STEPFUNCTIONS, config)
    assert isinstance(c, StepfunctionsClient)


@mock_aws
def test_create_and_describe_state_machine(config):
    role_arn = _create_role()
    client = typed_boto3.client(ServiceName.STEPFUNCTIONS, config)
    definition = json.dumps(
        {"StartAt": "End", "States": {"End": {"Type": "Pass", "End": True}}}
    )
    created = client.create_state_machine(
        CreateStateMachineInputTypeDef(
            name="my-sm", definition=definition, roleArn=role_arn
        )
    )
    assert created is not None
    resp = client.describe_state_machine(
        DescribeStateMachineInputTypeDef(stateMachineArn=created.stateMachineArn)
    )
    assert resp is not None
    assert resp.name == "my-sm"
