import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.runner import substitute_variables  # noqa: E402


def test_substitute_single_variable():
    result = substitute_variables("Hello {{name}}", {"name": "World"})
    assert result == "Hello World"


def test_substitute_multiple_variables():
    template = "{{sender}} sends {{action}} to {{target}}"
    variables = {"sender": "Alice", "action": "email", "target": "Bob"}
    result = substitute_variables(template, variables)
    assert result == "Alice sends email to Bob"


def test_substitute_missing_variable_keeps_placeholder():
    result = substitute_variables("Hello {{name}}", {})
    assert result == "Hello {{name}}"


def test_substitute_no_variables():
    result = substitute_variables("No variables here", {"name": "Test"})
    assert result == "No variables here"


def test_substitute_empty_template():
    result = substitute_variables("", {"name": "Test"})
    assert result == ""
