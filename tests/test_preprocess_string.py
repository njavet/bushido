from bushido.core.result import Err, Ok
from bushido.iface.parser.utils import preprocess_input


def test_empty_input_string():
    input_string = ''
    result = preprocess_input(input_string)
    assert isinstance(result, Err)
    assert result.message == 'empty payload'


def test_comment_symbol_only():
    input_string = '#'
    result = preprocess_input(input_string)
    assert isinstance(result, Err)
    assert result.message == 'empty payload'


def test_empty_payload():
    input_string = '# this is a comment'
    result = preprocess_input(input_string)
    assert isinstance(result, Err)
    assert result.message == 'empty payload'


def test_correct_input_syntax_without_comment():
    input_string = 'husserl some 101 char 5'
    result = preprocess_input(input_string)
    assert isinstance(result, Ok)
    assert result.value.name == 'husserl'
    assert result.value.words == ['some', '101', 'char', '5']
    assert result.value.comment is None


def test_correct_input_syntax_without_comment_but_symbol():
    input_string = 'platon 101 5 #'
    result = preprocess_input(input_string)
    assert isinstance(result, Ok)
    assert result.value.name == 'platon'
    assert result.value.words == ['101', '5']
    assert result.value.comment is None


def test_correct_input_syntax_full():
    input_string = 'schopenhauer some numbers eg 5 # this is a comment'
    result = preprocess_input(input_string)
    assert isinstance(result, Ok)
    assert result.value.name == 'schopenhauer'
    assert result.value.words == ['some', 'numbers', 'eg', '5']
    assert result.value.comment == 'this is a comment'


def test_correct_input_syntax_no_payload():
    input_string = 'kant # this is a comment'
    result = preprocess_input(input_string)
    assert isinstance(result, Ok)
    assert result.value.name == 'kant'
    assert result.value.words == []
    assert result.value.comment == 'this is a comment'


def test_correct_input_syntax_no_payload_no_comment():
    input_string = 'wittgenstein'
    result = preprocess_input(input_string)
    assert isinstance(result, Ok)
    assert result.value.name == 'wittgenstein'
    assert result.value.words == []
    assert result.value.comment is None
