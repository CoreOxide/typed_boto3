from typed_boto3.generator.discover import discover


def test_discover_lambda_has_create_function():
    ops = discover("lambda")
    by_method = {op.py_method: op for op in ops}
    assert "create_function" in by_method
    cf = by_method["create_function"]
    assert cf.api_name == "CreateFunction"
    assert cf.input_shape == "CreateFunctionRequest"
    assert cf.output_shape == "FunctionConfiguration"


def test_discover_s3_has_create_bucket():
    ops = discover("s3")
    by_method = {op.py_method: op for op in ops}
    assert "create_bucket" in by_method
    cb = by_method["create_bucket"]
    assert cb.api_name == "CreateBucket"
    assert cb.input_shape == "CreateBucketRequest"


def test_discover_returns_sorted_and_unique():
    ops = discover("lambda")
    methods = [op.py_method for op in ops]
    assert methods == sorted(methods)
    assert len(methods) == len(set(methods))
