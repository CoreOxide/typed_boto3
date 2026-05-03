from typed_boto3.generator.resolver import module_path, resolve


def test_module_path_lambda_is_keyword_suffixed():
    assert module_path("lambda") == "aws_resource_validator.pydantic_models.lambda_.lambda__classes"


def test_module_path_s3_plain():
    assert module_path("s3") == "aws_resource_validator.pydantic_models.s3.s3_classes"


def test_resolve_returns_hit_for_known_shape():
    r = resolve("lambda", "CreateFunctionRequest")
    assert r is not None
    assert r.class_name == "CreateFunctionRequestTypeDef"
    assert r.import_path == "aws_resource_validator.pydantic_models.lambda_.lambda__classes"


def test_resolve_returns_none_for_missing_shape():
    assert resolve("lambda", "ThisShapeDoesNotExist") is None


def test_resolve_returns_none_when_shape_is_none():
    assert resolve("lambda", None) is None
