"""typed_boto3 — strongly-typed, SDK-like wrapper around boto3."""

# --- BEGIN GENERATED ---
from typing import Literal, overload
from typed_boto3._service_name import ServiceName
from typed_boto3._region import Region
from typed_boto3.core.config import ClientConfig, AwsCredentials
from typed_boto3.services.lambda_client import LambdaClient
from typed_boto3.services.s3_client import S3Client

@overload
def client(service_name: Literal[ServiceName.LAMBDA], config: ClientConfig | None = None) -> LambdaClient: ...
@overload
def client(service_name: Literal[ServiceName.S3], config: ClientConfig | None = None) -> S3Client: ...

def client(service_name: ServiceName, config: ClientConfig | None = None) -> LambdaClient | S3Client:
    mapping: dict[ServiceName, type] = {
        ServiceName.LAMBDA: LambdaClient,
        ServiceName.S3: S3Client,
    }
    return mapping[service_name](config)  # type: ignore[no-any-return]

__all__ = ["client", "ServiceName", "Region", "ClientConfig", "AwsCredentials", "LambdaClient", "S3Client"]
# --- END GENERATED ---
