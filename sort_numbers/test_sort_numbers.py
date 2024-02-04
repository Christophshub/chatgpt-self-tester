import pytest
from sort_numbers import sort_numbers

@pytest.fixture
def sample_numbers():
    return [6, 5, 3, 1, 8, 7, 2, 4]

def test_sort_numbers(sample_numbers):
    sorted_numbers = sort_numbers(sample_numbers)
    assert sorted_numbers == [1, 2, 3, 4, 5, 6, 7, 8]
