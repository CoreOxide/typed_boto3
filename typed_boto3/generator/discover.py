from dataclasses import dataclass

import boto3


@dataclass(frozen=True)
class OperationSpec:
    py_method: str
    api_name: str
    input_shape: str | None
    output_shape: str | None


def discover(service: str) -> list[OperationSpec]:
    client = boto3.client(service, region_name="us-east-1")
    sm = client.meta.service_model
    out: list[OperationSpec] = []
    for py_name, api_name in sorted(client.meta.method_to_api_mapping.items()):
        op = sm.operation_model(api_name)
        out.append(
            OperationSpec(
                py_method=py_name,
                api_name=api_name,
                input_shape=op.input_shape.name if op.input_shape else None,
                output_shape=op.output_shape.name if op.output_shape else None,
            )
        )
    return out