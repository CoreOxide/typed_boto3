"""Without the type-ignore comments, this file must FAIL mypy.

Committed version silences the errors so mypy --strict reports clean.
"""
import typed_boto3
from typed_boto3 import ClientConfig

typed_boto3.client("lambda")  # type: ignore[call-overload]  # bad: str, not ServiceName
ClientConfig(region="us-east-1")  # type: ignore[arg-type]  # bad: str, not Region
