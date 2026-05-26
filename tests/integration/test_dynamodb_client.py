import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, DynamodbClient, Region, ServiceName
from aws_resource_validator.pydantic_models.dynamodb.dynamodb_classes import (
    AttributeDefinitionTypeDef,
    CreateTableInputTypeDef,
    DescribeTableInputTypeDef,
    KeySchemaElementTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_dynamodb_client(config):
    c = typed_boto3.client(ServiceName.DYNAMODB, config)
    assert isinstance(c, DynamodbClient)


@mock_aws
def test_create_and_describe_table(config):
    client = typed_boto3.client(ServiceName.DYNAMODB, config)
    client.create_table(
        CreateTableInputTypeDef(
            TableName="my-table",
            AttributeDefinitions=[AttributeDefinitionTypeDef(AttributeName="id", AttributeType="S")],
            KeySchema=[KeySchemaElementTypeDef(AttributeName="id", KeyType="HASH")],
            BillingMode="PAY_PER_REQUEST",
        )
    )
    resp = client.describe_table(DescribeTableInputTypeDef(TableName="my-table"))
    assert resp is not None
    assert resp.Table is not None
    assert resp.Table.TableName == "my-table"
