from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from typed_boto3.generator.discover import discover
from typed_boto3.generator.naming import class_name, enum_member, module_name, service_dir
from typed_boto3.generator.resolver import resolve


@dataclass(frozen=True)
class _MethodSpec:
    name: str
    request_cls: str | None
    response_cls: str | None


@dataclass(frozen=True)
class EmitStats:
    total: int
    fully_typed: int
    untyped_input: int
    untyped_output: int


_ENV = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "templates"),
    undefined=StrictUndefined,
    trim_blocks=False,
    lstrip_blocks=False,
)
_TEMPLATE = _ENV.get_template("service_client.py.jinja")


def emit_service(service: str, out_dir: Path) -> EmitStats:
    ops = discover(service)

    methods: list[_MethodSpec] = []
    imports: set[str] = set()
    untyped_input = untyped_output = 0

    for op in ops:
        req = resolve(service, op.input_shape)
        resp = resolve(service, op.output_shape)
        if op.input_shape is not None and req is None:
            untyped_input += 1
        if op.output_shape is not None and resp is None:
            untyped_output += 1
        if req is not None:
            imports.add(req.class_name)
        if resp is not None:
            imports.add(resp.class_name)
        methods.append(
            _MethodSpec(
                name=op.py_method,
                request_cls=req.class_name if req else None,
                response_cls=resp.class_name if resp else None,
            )
        )

    svc_dir = service_dir(service)
    rendered = _TEMPLATE.render(
        service_dir=svc_dir,
        service_module=f"{svc_dir}_classes",
        imported_classes=sorted(imports),
        class_name=class_name(service),
        enum_member=enum_member(service),
        methods=methods,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{module_name(service)}.py").write_text(rendered, encoding="utf-8")

    return EmitStats(
        total=len(ops),
        fully_typed=sum(1 for m in methods if m.request_cls is not None and m.response_cls is not None),
        untyped_input=untyped_input,
        untyped_output=untyped_output,
    )
