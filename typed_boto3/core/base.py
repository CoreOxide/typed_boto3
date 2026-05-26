import functools
import typing
from typing import Any, TypeVar

import boto3
from pydantic import AliasChoices, BaseModel, TypeAdapter, ValidationError

from typed_boto3._service_name import ServiceName
from typed_boto3.core.config import ClientConfig

TResp = TypeVar("TResp", bound=BaseModel)


@functools.lru_cache(maxsize=None)
def _adapter_for(annotation: Any) -> TypeAdapter[Any]:
    return TypeAdapter(annotation)


def _basemodel_in(annotation: Any) -> type[BaseModel] | None:
    """Return the first BaseModel subclass found in an annotation, peeling
    Optional/Union/List/Sequence wrappers. Used to decide whether a failing
    strict validation should retry recursively in lenient mode.
    """
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return annotation
    for arg in typing.get_args(annotation):
        found = _basemodel_in(arg)
        if found is not None:
            return found
    return None


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
                value = raw[key]
                try:
                    values[name] = _adapter_for(annotation).validate_python(value)
                except ValidationError:
                    nested = _basemodel_in(annotation)
                    if nested is not None:
                        coerced = _lenient_coerce(annotation, nested, value)
                        if coerced is not _DROP:
                            values[name] = coerced
                break
    return response_cls.model_construct(**values)


_DROP: Any = object()


def _lenient_coerce(annotation: Any, model_cls: type[BaseModel], value: Any) -> Any:
    """Coerce `value` against `annotation` lazily — descend into lists/tuples
    and apply `_lenient_validate(model_cls, item)` to dicts. Returns _DROP
    when the value's shape doesn't match the annotation (e.g. a string where
    a model is expected) so callers can omit the field entirely rather than
    storing a raw, untyped value.
    """
    if isinstance(value, list | tuple):
        item_model = _list_item_basemodel(annotation) or model_cls
        coerced: list[Any] = []
        for item in value:
            if isinstance(item, dict):
                coerced.append(_lenient_validate(item_model, item))
            elif isinstance(item, item_model):
                coerced.append(item)
            else:
                return _DROP
        return tuple(coerced) if isinstance(value, tuple) else coerced
    if isinstance(value, dict):
        return _lenient_validate(model_cls, value)
    return _DROP


def _list_item_basemodel(annotation: Any) -> type[BaseModel] | None:
    """Find a `list[BaseModel]` (or tuple) inside an annotation and return
    the BaseModel item type, peeling Union/Optional wrappers."""
    origin = typing.get_origin(annotation)
    if origin in (list, tuple):
        for arg in typing.get_args(annotation):
            found = _basemodel_in(arg)
            if found is not None:
                return found
    for arg in typing.get_args(annotation):
        found = _list_item_basemodel(arg)
        if found is not None:
            return found
    return None
