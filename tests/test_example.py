
"""
COVERAGE
To generate a coverage report, run the following command in the root directory of the project:
    coverage run --source=. -m pytest
and then either/or to generate a html/xml report:
    coverage report
    coverage xml
"""
import pytest

def test_example():
    assert 1 == 1
