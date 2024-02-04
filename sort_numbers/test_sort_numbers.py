import pytest
from sort_numbers import sort_numbers

@pytest.fixture
def numbers():
    return [4, 2, 9, 6, 5, 1, 8, 7, 3]

def test_sort_numbers(numbers):
    assert sort_numbers(numbers) == sorted(numbers)
