import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import ClientConfig, RdsClient, Region, ServiceName
from aws_resource_validator.pydantic_models.rds.rds_classes import (
    CreateDBInstanceMessageTypeDef,
    DescribeDBInstancesMessageTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_rds_client(config):
    c = typed_boto3.client(ServiceName.RDS, config)
    assert isinstance(c, RdsClient)


@mock_aws
def test_create_and_describe_db_instance(config):
    client = typed_boto3.client(ServiceName.RDS, config)
    client.create_db_instance(
        CreateDBInstanceMessageTypeDef(
            DBInstanceIdentifier="my-db",
            DBInstanceClass="db.t3.micro",
            Engine="postgres",
            MasterUsername="admin",
            MasterUserPassword="hunter2hunter2",
            AllocatedStorage=20,
        )
    )
    resp = client.describe_db_instances(
        DescribeDBInstancesMessageTypeDef(DBInstanceIdentifier="my-db")
    )
    assert resp is not None
    assert resp.DBInstances is not None
    assert len(resp.DBInstances) == 1
    assert resp.DBInstances[0].DBInstanceIdentifier == "my-db"
