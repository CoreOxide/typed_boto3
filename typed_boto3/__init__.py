"""typed_boto3 — strongly-typed, SDK-like wrapper around boto3."""

# --- BEGIN GENERATED ---
from typing import Literal, overload
from typed_boto3._service_name import ServiceName
from typed_boto3._region import Region
from typed_boto3.core.config import ClientConfig, AwsCredentials
from typed_boto3.services.s3_client import S3Client
from typed_boto3.services.lambda_client import LambdaClient
from typed_boto3.services.ec2_client import Ec2Client
from typed_boto3.services.dynamodb_client import DynamodbClient
from typed_boto3.services.iam_client import IamClient
from typed_boto3.services.sts_client import StsClient
from typed_boto3.services.cloudwatch_client import CloudwatchClient
from typed_boto3.services.logs_client import LogsClient
from typed_boto3.services.sns_client import SnsClient
from typed_boto3.services.sqs_client import SqsClient
from typed_boto3.services.kms_client import KmsClient
from typed_boto3.services.secretsmanager_client import SecretsmanagerClient
from typed_boto3.services.ssm_client import SsmClient
from typed_boto3.services.stepfunctions_client import StepfunctionsClient
from typed_boto3.services.ecs_client import EcsClient
from typed_boto3.services.rds_client import RdsClient
from typed_boto3.services.elbv2_client import Elbv2Client
from typed_boto3.services.apigateway_client import ApigatewayClient
from typed_boto3.services.apigatewayv2_client import Apigatewayv2Client
from typed_boto3.services.cloudformation_client import CloudformationClient
from typed_boto3.services.events_client import EventsClient
from typed_boto3.services.kinesis_client import KinesisClient
from typed_boto3.services.firehose_client import FirehoseClient
from typed_boto3.services.glue_client import GlueClient
from typed_boto3.services.athena_client import AthenaClient
from typed_boto3.services.redshift_client import RedshiftClient
from typed_boto3.services.sagemaker_client import SagemakerClient
from typed_boto3.services.bedrock_client import BedrockClient
from typed_boto3.services.cognito_idp_client import CognitoIdpClient
from typed_boto3.services.route53_client import Route53Client

@overload
def client(service_name: Literal[ServiceName.S3], config: ClientConfig | None = None) -> S3Client: ...
@overload
def client(service_name: Literal[ServiceName.LAMBDA], config: ClientConfig | None = None) -> LambdaClient: ...
@overload
def client(service_name: Literal[ServiceName.EC2], config: ClientConfig | None = None) -> Ec2Client: ...
@overload
def client(service_name: Literal[ServiceName.DYNAMODB], config: ClientConfig | None = None) -> DynamodbClient: ...
@overload
def client(service_name: Literal[ServiceName.IAM], config: ClientConfig | None = None) -> IamClient: ...
@overload
def client(service_name: Literal[ServiceName.STS], config: ClientConfig | None = None) -> StsClient: ...
@overload
def client(service_name: Literal[ServiceName.CLOUDWATCH], config: ClientConfig | None = None) -> CloudwatchClient: ...
@overload
def client(service_name: Literal[ServiceName.LOGS], config: ClientConfig | None = None) -> LogsClient: ...
@overload
def client(service_name: Literal[ServiceName.SNS], config: ClientConfig | None = None) -> SnsClient: ...
@overload
def client(service_name: Literal[ServiceName.SQS], config: ClientConfig | None = None) -> SqsClient: ...
@overload
def client(service_name: Literal[ServiceName.KMS], config: ClientConfig | None = None) -> KmsClient: ...
@overload
def client(service_name: Literal[ServiceName.SECRETSMANAGER], config: ClientConfig | None = None) -> SecretsmanagerClient: ...
@overload
def client(service_name: Literal[ServiceName.SSM], config: ClientConfig | None = None) -> SsmClient: ...
@overload
def client(service_name: Literal[ServiceName.STEPFUNCTIONS], config: ClientConfig | None = None) -> StepfunctionsClient: ...
@overload
def client(service_name: Literal[ServiceName.ECS], config: ClientConfig | None = None) -> EcsClient: ...
@overload
def client(service_name: Literal[ServiceName.RDS], config: ClientConfig | None = None) -> RdsClient: ...
@overload
def client(service_name: Literal[ServiceName.ELBV2], config: ClientConfig | None = None) -> Elbv2Client: ...
@overload
def client(service_name: Literal[ServiceName.APIGATEWAY], config: ClientConfig | None = None) -> ApigatewayClient: ...
@overload
def client(service_name: Literal[ServiceName.APIGATEWAYV2], config: ClientConfig | None = None) -> Apigatewayv2Client: ...
@overload
def client(service_name: Literal[ServiceName.CLOUDFORMATION], config: ClientConfig | None = None) -> CloudformationClient: ...
@overload
def client(service_name: Literal[ServiceName.EVENTS], config: ClientConfig | None = None) -> EventsClient: ...
@overload
def client(service_name: Literal[ServiceName.KINESIS], config: ClientConfig | None = None) -> KinesisClient: ...
@overload
def client(service_name: Literal[ServiceName.FIREHOSE], config: ClientConfig | None = None) -> FirehoseClient: ...
@overload
def client(service_name: Literal[ServiceName.GLUE], config: ClientConfig | None = None) -> GlueClient: ...
@overload
def client(service_name: Literal[ServiceName.ATHENA], config: ClientConfig | None = None) -> AthenaClient: ...
@overload
def client(service_name: Literal[ServiceName.REDSHIFT], config: ClientConfig | None = None) -> RedshiftClient: ...
@overload
def client(service_name: Literal[ServiceName.SAGEMAKER], config: ClientConfig | None = None) -> SagemakerClient: ...
@overload
def client(service_name: Literal[ServiceName.BEDROCK], config: ClientConfig | None = None) -> BedrockClient: ...
@overload
def client(service_name: Literal[ServiceName.COGNITO_IDP], config: ClientConfig | None = None) -> CognitoIdpClient: ...
@overload
def client(service_name: Literal[ServiceName.ROUTE53], config: ClientConfig | None = None) -> Route53Client: ...

def client(service_name: ServiceName, config: ClientConfig | None = None) -> S3Client | LambdaClient | Ec2Client | DynamodbClient | IamClient | StsClient | CloudwatchClient | LogsClient | SnsClient | SqsClient | KmsClient | SecretsmanagerClient | SsmClient | StepfunctionsClient | EcsClient | RdsClient | Elbv2Client | ApigatewayClient | Apigatewayv2Client | CloudformationClient | EventsClient | KinesisClient | FirehoseClient | GlueClient | AthenaClient | RedshiftClient | SagemakerClient | BedrockClient | CognitoIdpClient | Route53Client:
    mapping: dict[ServiceName, type] = {
        ServiceName.S3: S3Client,
        ServiceName.LAMBDA: LambdaClient,
        ServiceName.EC2: Ec2Client,
        ServiceName.DYNAMODB: DynamodbClient,
        ServiceName.IAM: IamClient,
        ServiceName.STS: StsClient,
        ServiceName.CLOUDWATCH: CloudwatchClient,
        ServiceName.LOGS: LogsClient,
        ServiceName.SNS: SnsClient,
        ServiceName.SQS: SqsClient,
        ServiceName.KMS: KmsClient,
        ServiceName.SECRETSMANAGER: SecretsmanagerClient,
        ServiceName.SSM: SsmClient,
        ServiceName.STEPFUNCTIONS: StepfunctionsClient,
        ServiceName.ECS: EcsClient,
        ServiceName.RDS: RdsClient,
        ServiceName.ELBV2: Elbv2Client,
        ServiceName.APIGATEWAY: ApigatewayClient,
        ServiceName.APIGATEWAYV2: Apigatewayv2Client,
        ServiceName.CLOUDFORMATION: CloudformationClient,
        ServiceName.EVENTS: EventsClient,
        ServiceName.KINESIS: KinesisClient,
        ServiceName.FIREHOSE: FirehoseClient,
        ServiceName.GLUE: GlueClient,
        ServiceName.ATHENA: AthenaClient,
        ServiceName.REDSHIFT: RedshiftClient,
        ServiceName.SAGEMAKER: SagemakerClient,
        ServiceName.BEDROCK: BedrockClient,
        ServiceName.COGNITO_IDP: CognitoIdpClient,
        ServiceName.ROUTE53: Route53Client,
    }
    return mapping[service_name](config)  # type: ignore[no-any-return]

__all__ = ["client", "ServiceName", "Region", "ClientConfig", "AwsCredentials", "S3Client", "LambdaClient", "Ec2Client", "DynamodbClient", "IamClient", "StsClient", "CloudwatchClient", "LogsClient", "SnsClient", "SqsClient", "KmsClient", "SecretsmanagerClient", "SsmClient", "StepfunctionsClient", "EcsClient", "RdsClient", "Elbv2Client", "ApigatewayClient", "Apigatewayv2Client", "CloudformationClient", "EventsClient", "KinesisClient", "FirehoseClient", "GlueClient", "AthenaClient", "RedshiftClient", "SagemakerClient", "BedrockClient", "CognitoIdpClient", "Route53Client"]
# --- END GENERATED ---
