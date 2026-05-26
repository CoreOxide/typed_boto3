import typed_boto3
from typed_boto3 import BedrockClient, ClientConfig, Region, ServiceName


def test_factory_returns_bedrock_client():
    config = ClientConfig(region=Region.US_EAST_1)
    c = typed_boto3.client(ServiceName.BEDROCK, config)
    assert isinstance(c, BedrockClient)


def test_direct_client_class_instantiation():
    config = ClientConfig(region=Region.US_EAST_1)
    c = BedrockClient(config)
    assert c.raw is not None
