import pytest

# project imports
from bushido.domain.unit import UnitSpec
from bushido.service.log_unit import LogUnitService


@pytest.fixture
def service():
    return LogUnitService()


def test_empty_input_string(service):
    input_string = ''
    with pytest.raises(ValueError):
        service.preprocess_input(input_string)


def test_comment_symbol_only(service):
    input_string = '#'
    with pytest.raises(ValueError):
        service.preprocess_input(input_string)


def test_empty_payload(service):
    input_string = '# this is a comment'
    with pytest.raises(ValueError):
        service.preprocess_input(input_string)


def test_correct_input_syntax_without_comment(service):
    input_string = 'husserl some 101 char 5'
    unit_spec = service.preprocess_input(input_string)
    assert unit_spec.unit_name == 'husserl'
    assert unit_spec.words == ['some', '101', 'char', '5']
    assert unit_spec.comment is None


def test_correct_input_syntax_without_comment_but_symbol(service):
    input_string = 'platon 101 5 #'
    unit_spec = service.preprocess_input(input_string)
    assert unit_spec.unit_name == 'platon'
    assert unit_spec.words == ['101', '5']
    assert unit_spec.comment is None


def test_correct_input_syntax_full(service):
    input_string = 'schopenhauer some numbers eg 5 # this is a comment'
    unit_spec = service.preprocess_input(input_string)
    assert unit_spec.unit_name == 'schopenhauer'
    assert unit_spec.words == ['some', 'numbers', 'eg', '5']
    assert unit_spec.comment == 'this is a comment'


def test_correct_input_syntax_no_payload(service):
    input_string = 'kant # this is a comment'
    unit_spec = service.preprocess_input(input_string)
    assert unit_spec.unit_name == 'kant'
    assert unit_spec.words == []
    assert unit_spec.comment == 'this is a comment'


def test_correct_input_syntax_no_payload_no_comment(service):
    input_string = 'wittgenstein'
    unit_spec = service.preprocess_input(input_string)
    assert unit_spec.unit_name == 'wittgenstein'
    assert unit_spec.words == []
    assert unit_spec.comment is None

