from __future__ import annotations

import pytest

from textual.validation import (
    URL,
    Failure,
    Function,
    Integer,
    Length,
    Number,
    Regex,
    ValidationResult,
    Validator,
)

VALIDATOR = Function(lambda value: True)


class ValidatorWithDescribeFailure(Validator):
    def validate(self, value: str) -> ValidationResult:
        return self.failure()

    def describe_failure(self, failure: Failure) -> str | None:
        return "describe_failure"


class ValidatorWithFailureMessageAndNoDescribe(Validator):
    def validate(self, value: str) -> ValidationResult:
        return self.failure(description="ABC")


class ValidatorWithFailureMessageAndDescribe(Validator):
    def validate(self, value: str) -> ValidationResult:
        return self.failure(value=value, description="ABC")

    def describe_failure(self, failure: Failure) -> str | None:
        return "describe_failure"


@pytest.mark.parametrize(
    "function, failure_description, is_valid",
    [
        ((lambda value: True), None, True),
        ((lambda value: False), "failure!", False),
    ],
)
def test_Function_validate(function, failure_description, is_valid):
    validator = Function(function, failure_description)
    result = validator.validate("x")
    assert result.is_valid is is_valid
    if result.failure_descriptions:
        assert result.failure_descriptions[0] == failure_description


def test_Integer_failure_description_when_NotANumber():
    """Regression test for https://github.com/Textualize/textual/issues/4413"""
    validator = Integer()
    result = validator.validate("x")
    assert result.is_valid is False
    assert result.failure_descriptions[0] == "Must be a valid integer."
