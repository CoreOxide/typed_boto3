import pytest
from moto import mock_aws

import typed_boto3
from typed_boto3 import AthenaClient, ClientConfig, Region, ServiceName
from aws_resource_validator.pydantic_models.athena.athena_classes import (
    GetQueryExecutionInputTypeDef,
    StartQueryExecutionInputTypeDef,
)


@pytest.fixture
def config() -> ClientConfig:
    return ClientConfig(region=Region.US_EAST_1)


@mock_aws
def test_factory_returns_athena_client(config):
    c = typed_boto3.client(ServiceName.ATHENA, config)
    assert isinstance(c, AthenaClient)


@mock_aws
def test_start_and_get_query_execution(config):
    client = typed_boto3.client(ServiceName.ATHENA, config)
    started = client.start_query_execution(
        StartQueryExecutionInputTypeDef(QueryString="SELECT 1")
    )
    assert started is not None
    qid = started.QueryExecutionId
    assert qid is not None
    resp = client.get_query_execution(GetQueryExecutionInputTypeDef(QueryExecutionId=qid))
    assert resp is not None
    assert resp.QueryExecution is not None
    assert resp.QueryExecution.QueryExecutionId == qid
