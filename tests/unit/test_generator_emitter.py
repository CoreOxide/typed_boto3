import ast

from typed_boto3.generator.emitter import emit_service


def test_emitter_produces_parseable_python(tmp_path):
    stats = emit_service("lambda", tmp_path)
    out = tmp_path / "lambda_client.py"
    assert out.exists()
    source = out.read_text()
    tree = ast.parse(source)
    # Must define exactly one class named LambdaClient
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    assert [c.name for c in classes] == ["LambdaClient"]
    # That class must contain a create_function method
    methods = {n.name for n in classes[0].body if isinstance(n, ast.FunctionDef)}
    assert "create_function" in methods
    assert "get_function" in methods
    assert stats.total > 50


def test_emitter_s3(tmp_path):
    emit_service("s3", tmp_path)
    out = tmp_path / "s3_client.py"
    ast.parse(out.read_text())  # must parse
    assert "class S3Client(TypedClientBase)" in out.read_text()
