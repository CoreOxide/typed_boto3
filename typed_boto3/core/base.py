import functools
from typing import Any, TypeVar

import boto3
from pydantic import AliasChoices, BaseModel, TypeAdapter, ValidationError

from typed_boto3._service_name import ServiceName
from typed_boto3.core.config import ClientConfig

TResp = TypeVar("TResp", bound=BaseModel)


@functools.lru_cache(maxsize=None)
def _adapter_for(annotation: Any) -> TypeAdapter[Any]:
    return TypeAdapter(annotation)


class TypedClientBase:
    """Base class for generated service clients.

    Holds a boto3 client and dispatches typed request/response models through
    `_call`, falling back to `_lenient_validate` when upstream models are
    stricter than real AWS responses.
    """

    _service_name: ServiceName

    def __init__(self, config: ClientConfig | None = None) -> None:
        kwargs = config.to_boto_kwargs() if config is not None else {}
        self._client = boto3.client(self._service_name.value, **kwargs)

    def _call(
        self,
        method_name: str,
        request: BaseModel | None,
        response_cls: type[TResp] | None,
    ) -> TResp | None:
        payload = request.model_dump(exclude_none=True, by_alias=True) if request is not None else {}
        raw = getattr(self._client, method_name)(**payload)
        if response_cls is None:
            return None
        try:
            return response_cls.model_validate(raw)
        except ValidationError:
            return _lenient_validate(response_cls, raw)

    @property
    def raw(self) -> Any:
        return self._client


def _field_lookup_keys(name: str, field: Any) -> tuple[str, ...]:
    """Return the payload keys to try for a given model field, in priority order."""
    candidates: list[str] = []
    va = getattr(field, "validation_alias", None)
    if isinstance(va, AliasChoices):
        candidates.extend(c for c in va.choices if isinstance(c, str))
    elif isinstance(va, str):
        candidates.append(va)
    alias = getattr(field, "alias", None)
    if isinstance(alias, str):
        candidates.append(alias)
    candidates.append(name)
    seen: set[str] = set()
    unique: list[str] = []
    for key in candidates:
        if key not in seen:
            seen.add(key)
            unique.append(key)
    return tuple(unique)


def _lenient_validate(response_cls: type[TResp], raw: dict[str, Any]) -> TResp:
    """Build a response by validating only fields actually present in the payload.

    Upstream Pydantic models in `aws_resource_validator` occasionally mark
    fields required that real AWS responses leave absent. This fallback
    validates each present field individually; any field whose value fails
    validation (or whose type cannot be coerced) is dropped rather than
    substituting a raw untyped value, so callers don't see a declared
    `SubModel` instance that is actually a `dict`.
    """
    values: dict[str, Any] = {}
    for name, field in response_cls.model_fields.items():
        annotation: Any = field.annotation
        if annotation is None:
            continue
        for key in _field_lookup_keys(name, field):
            if key in raw:
                try:
                    values[name] = _adapter_for(annotation).validate_python(raw[key])
                except ValidationError:
                    pass
                break
    return response_cls.model_construct(**values)
