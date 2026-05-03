import ast

from typed_boto3.generator.overloads_emitter import (
    BEGIN,
    END,
    write_package_init,
    write_service_name_enum,
    write_services_init,
)


def test_write_service_name_enum(tmp_path):
    write_service_name_enum(["lambda", "s3"], tmp_path)
    src = (tmp_path / "_service_name.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    class_def = next(n for n in tree.body if isinstance(n, ast.ClassDef))
    assert class_def.name == "ServiceName"
    members = {n.targets[0].id for n in class_def.body if isinstance(n, ast.Assign)}
    assert members == {"LAMBDA", "S3"}


def test_write_services_init(tmp_path):
    write_services_init(["lambda", "s3"], tmp_path)
    src = (tmp_path / "__init__.py").read_text(encoding="utf-8")
    assert "from typed_boto3.services.lambda_client import LambdaClient" in src
    assert "from typed_boto3.services.s3_client import S3Client" in src
    assert '__all__ = ["LambdaClient", "S3Client"]' in src


def test_write_package_init_renders_overloads(tmp_path):
    write_package_init(["lambda", "s3"], tmp_path)
    src = (tmp_path / "__init__.py").read_text(encoding="utf-8")
    assert BEGIN in src and END in src
    assert src.count("@overload") == 2
    assert "Literal[ServiceName.LAMBDA]" in src
    assert "Literal[ServiceName.S3]" in src
    # Ensure the whole file parses and the factory is defined.
    tree = ast.parse(src)
    fns = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "client"]
    assert len(fns) == 3  # two @overloads + one impl


def test_write_package_init_preserves_content_outside_markers(tmp_path):
    init_path = tmp_path / "__init__.py"
    init_path.write_text(
        '"""preserved docstring."""\n'
        "CUSTOM_BEFORE = 1\n"
        f"{BEGIN}\n# old body\n{END}\n"
        "CUSTOM_AFTER = 2\n",
        encoding="utf-8",
    )
    write_package_init(["lambda"], tmp_path)
    src = init_path.read_text(encoding="utf-8")
    assert "preserved docstring" in src
    assert "CUSTOM_BEFORE = 1" in src
    assert "CUSTOM_AFTER = 2" in src
    assert "# old body" not in src
    assert "Literal[ServiceName.LAMBDA]" in src


def test_write_package_init_seeds_default_header_when_no_markers(tmp_path):
    # Fresh directory (no existing __init__.py) — default header is written.
    write_package_init(["lambda"], tmp_path)
    src = (tmp_path / "__init__.py").read_text(encoding="utf-8")
    assert src.startswith('"""typed_boto3')
    assert BEGIN in src and END in src
