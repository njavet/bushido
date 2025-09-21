import pytest

# project imports
from bushido.core.result import Ok, Err
from bushido.service.log_unit import LogUnitService


@pytest.fixture
def service():
    return LogUnitService()


def test_empty_input_string(service):
    input_string = ''
    result = service.preprocess_input(input_string)
    assert isinstance(result, Err)
    assert result.message == 'empty payload'


def test_comment_symbol_only(service):
    input_string = '#'
    result = service.preprocess_input(input_string)
    assert isinstance(result, Err)
    assert result.message == 'empty payload'


def test_empty_payload(service):
    input_string = '# this is a comment'
    result = service.preprocess_input(input_string)
    assert isinstance(result, Err)
    assert result.message == 'empty payload'


def test_correct_input_syntax_without_comment(service):
    input_string = 'husserl some 101 char 5'
    result = service.preprocess_input(input_string)
    assert isinstance(result, Ok)
    assert result.value.unit_name == 'husserl'
    assert result.value.words == ['some', '101', 'char', '5']
    assert result.value.comment is None


def test_correct_input_syntax_without_comment_but_symbol(service):
    input_string = 'platon 101 5 #'
    result = service.preprocess_input(input_string)
    assert isinstance(result, Ok)
    assert result.value.unit_name == 'platon'
    assert result.value.words == ['101', '5']
    assert result.value.comment is None


def test_correct_input_syntax_full(service):
    input_string = 'schopenhauer some numbers eg 5 # this is a comment'
    result = service.preprocess_input(input_string)
    assert isinstance(result, Ok)
    assert result.value.unit_name == 'schopenhauer'
    assert result.value.words == ['some', 'numbers', 'eg', '5']
    assert result.value.comment == 'this is a comment'


def test_correct_input_syntax_no_payload(service):
    input_string = 'kant # this is a comment'
    result = service.preprocess_input(input_string)
    assert isinstance(result, Ok)
    assert result.value.unit_name == 'kant'
    assert result.value.words == []
    assert result.value.comment == 'this is a comment'


def test_correct_input_syntax_no_payload_no_comment(service):
    input_string = 'wittgenstein'
    result = service.preprocess_input(input_string)
    assert isinstance(result, Ok)
    assert result.value.unit_name == 'wittgenstein'
    assert result.value.words == []
    assert result.value.comment is None

