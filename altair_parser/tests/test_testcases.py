"""
These tests iterate through the examples defined in _testcases.py and make
sure each passes with both altair_parser and jsonschema
"""

import traitlets as T
import jsonschema
import pytest

from .. import JSONSchema
from ..utils import load_dynamic_module
from . import _testcases

testcases = {key: getattr(_testcases, key)
             for key in dir(_testcases)
             if not key.startswith('_')}


@pytest.mark.parametrize('testcase', testcases.keys())
def test_testcases_jsonschema(testcase):
    testcase = testcases[testcase]

    schema = testcase['schema']
    valid = testcase['valid']
    invalid = testcase.get('invalid', [])

    for instance in valid:
        jsonschema.validate(instance, schema)
    for instance in invalid:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance, schema)


@pytest.mark.parametrize('testcase', testcases.keys())
def test_testcases_traitlets(testcase):
    testcase = testcases[testcase]

    schema = testcase['schema']
    valid = testcase['valid']
    invalid = testcase.get('invalid', [])

    traitlets_obj = JSONSchema(schema)
    schema = load_dynamic_module(traitlets_obj.module_spec())

    for instance in valid:
        schema.RootInstance(**instance)
    for instance in invalid:
        with pytest.raises(T.TraitError):
            schema.RootInstance(**instance)