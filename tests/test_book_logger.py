import pytest
import src.book_logger as book_logger
import os

# Get users home directory
home_directory = os.path.expanduser('~')


def test_json_as_not_found():
    json_path = os.path.join(os.path.dirname(__file__), "fake-json-file.json")
    with pytest.raises(FileNotFoundError):
        open(json_path)



