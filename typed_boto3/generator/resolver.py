import functools
import importlib
from dataclasses import dataclass
from types import ModuleType

from typed_boto3.generator.naming import service_dir


@dataclass(frozen=True)
class ResolvedClass:
    import_path: str
    class_name: str


def module_path(service: str) -> str:
    svc = service_dir(service)
    return f"aws_resource_validator.pydantic_models.{svc}.{svc}_classes"


@functools.lru_cache(maxsize=None)
def _load_module(path: str) -> ModuleType | None:
    try:
        return importlib.import_module(path)
    except ModuleNotFoundError:
        return None


def resolve(service: str, shape_name: str | None) -> ResolvedClass | None:
    if shape_name is None:
        return None
    path = module_path(service)
    mod = _load_module(path)
    if mod is None:
        return None
    class_name = f"{shape_name}TypeDef"
    if not hasattr(mod, class_name):
        return None
    return ResolvedClass(import_path=path, class_name=class_name)