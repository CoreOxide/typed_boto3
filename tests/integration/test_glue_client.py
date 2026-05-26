import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, GlueClient, Region, ServiceName
from aws_resource_validator.pydantic_models.glue.glue_classes import (
    CreateDatabaseRequestTypeDef,
    DatabaseInputTypeDef,
    GetDatabasesRequestTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_glue_client(config):
    c = typed_boto3.client(ServiceName.GLUE, config)
    assert isinstance(c, GlueClient)


@mock_aws
def test_create_and_get_databases(config):
    client = typed_boto3.client(ServiceName.GLUE, config)
    client.create_database(
        CreateDatabaseRequestTypeDef(DatabaseInput=DatabaseInputTypeDef(Name="mydb"))
    )
    resp = client.get_databases(GetDatabasesRequestTypeDef())
    assert resp is not None
    assert resp.DatabaseList is not None
    names = [d.Name for d in resp.DatabaseList]
    assert "mydb" in names
