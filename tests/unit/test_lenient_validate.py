from pydantic import AliasChoices, BaseModel, Field

from typed_boto3.core.base import _lenient_validate


class Inner(BaseModel):
    n: int


class Outer(BaseModel):
    required_missing: str
    name: str | None = None
    nested: Inner | None = None


def test_missing_required_field_is_dropped():
    built = _lenient_validate(Outer, {"name": "x"})
    assert built.name == "x"
    assert "required_missing" not in built.model_fields_set


def test_nested_dict_becomes_model_instance():
    built = _lenient_validate(Outer, {"nested": {"n": 3}})
    assert isinstance(built.nested, Inner)
    assert built.nested.n == 3


def test_untyped_fallback_is_dropped_not_stored_raw():
    # "nested" declared as Inner but payload sends a string — cannot validate,
    # so the field must not end up populated with a raw str.
    built = _lenient_validate(Outer, {"nested": "not-a-dict"})
    assert "nested" not in built.model_fields_set


class Aliased(BaseModel):
    http_status: int = Field(alias="HTTPStatus")


def test_alias_resolution():
    built = _lenient_validate(Aliased, {"HTTPStatus": 200})
    assert built.http_status == 200


class ValidationAliased(BaseModel):
    kind: str = Field(validation_alias=AliasChoices("Kind", "type"))


def test_validation_alias_choices_resolved():
    built = _lenient_validate(ValidationAliased, {"type": "foo"})
    assert built.kind == "foo"

    built2 = _lenient_validate(ValidationAliased, {"Kind": "bar"})
    assert built2.kind == "bar"


class StrictInner(BaseModel):
    a: int
    b: int  # required, but real payload omits it


class HasStrictNested(BaseModel):
    nested: StrictInner | None = None


class HasStrictNestedList(BaseModel):
    items: list[StrictInner] | None = None


def test_nested_with_missing_required_field_falls_back_to_lenient():
    # Strict validation fails because b is missing — lenient should still
    # produce a StrictInner with a populated, b dropped.
    built = _lenient_validate(HasStrictNested, {"nested": {"a": 1}})
    assert isinstance(built.nested, StrictInner)
    assert built.nested.a == 1
    assert "b" not in built.nested.model_fields_set


def test_list_of_nested_models_recurses_per_item():
    built = _lenient_validate(HasStrictNestedList, {"items": [{"a": 1}, {"a": 2}]})
    assert built.items is not None
    assert len(built.items) == 2
    assert all(isinstance(i, StrictInner) for i in built.items)
    assert [i.a for i in built.items] == [1, 2]
