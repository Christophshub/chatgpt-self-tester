# test_sort_list.py

import pytest
from sort_numbers import sort_numbers    # adjust this import according to where your sort_numbers method is located

@pytest.fixture
def input_data():
    return [9, 3, 6, 1, 4, 0, 5]

@pytest.fixture
def sorted_data():
    return [0, 1, 3, 4, 5, 6, 9]

def test_sort_numbers(input_data, sorted_data):
    assert sort_numbers(input_data) == sorted_data
