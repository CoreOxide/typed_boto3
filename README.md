# typed_boto3

A strongly-typed, SDK-like wrapper around `boto3`. Inputs and outputs on every
client method are concrete Pydantic models — no dicts, no magic strings.

## Install

```bash
poetry install
```

`typed_boto3` depends on [`aws-resource-validator`](https://pypi.org/project/aws-resource-validator/)
for the generated Pydantic models that describe every AWS request/response shape.

## Usage

```python
import typed_boto3
from typed_boto3 import ServiceName, Region, ClientConfig
from aws_resource_validator.pydantic_models.lambda_.lambda__classes import (
    CreateFunctionRequestTypeDef,
    FunctionCodeTypeDef,
)

config = ClientConfig(region=Region.US_EAST_1)
client = typed_boto3.client(ServiceName.LAMBDA, config)  # typed as LambdaClient

resp = client.create_function(
    CreateFunctionRequestTypeDef(
        FunctionName="my-fn",
        Runtime="python3.11",
        Role="arn:aws:iam::123456789012:role/my-role",
        Handler="app.handler",
        Code=FunctionCodeTypeDef(ZipFile=b"..."),
    )
)
# resp is a FunctionConfigurationResponseTypeDef
print(resp.FunctionArn)
```

The direct form is also supported:

```python
from typed_boto3 import LambdaClient
client = LambdaClient(ClientConfig(region=Region.US_EAST_1))
```

## Regenerating

```bash
poetry run python -m typed_boto3.generator --regions
poetry run python -m typed_boto3.generator --service lambda s3
```
