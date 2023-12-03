from unittest.mock import patch
import builtins
import os
import json
import tempfile
from src import book_logger
"""
I honestly have no idea how good these tests are, this is the first time I've ever tried creating unit tests and it's 
more confusing to me than writing the initial code, but I just asked chatGPT to make me some test functions so idk. I'm
so used to manually testing my code, this is supposed to be faster but also I have no idea what's going on.
"""


def main():
    test_check_data_structure()
    test_is_file_empty()
    test_add_file_header()
    test_check_start_date_user_wants_to_enter_start_date()
    test_check_start_date_user_does_not_want_to_enter_start_date()
    test_check_start_date_already_exists()
    test_modify_entry_quit()
    test_modify_author_existing_author()
    test_modify_author_exit_command()
    test_modify_book_exit_command()
    test_modify_book_valid_input()
    test_modify_book_existing_book()
    test_import_JSON_PATH()
    test_import_existing_json()
    test_import_nonexistent_json()


def test_check_data_structure():
    # Initialize an empty data structure
    data = {}

    # Call the function with new author and novel
    author = "John Doe"
    novel = "The Great Novel"
    book_logger.check_data_structure(data, author, novel)

    # Check if the structure has been updated as expected
    assert author in data
    assert novel in data[author]
    assert data[author][novel] == {}

    # Call the function with an existing author and novel
    book_logger.check_data_structure(data, author, novel)

    # Check if the structure remains unchanged
    assert author in data
    assert novel in data[author]
    assert data[author][novel] == {}

    # Call the function with a new author and different novel
    novel2 = "The Greater Novel"
    book_logger.check_data_structure(data, author, novel2)

    # Check if the structure has been updated with the new novel
    assert author in data
    assert novel2 in data[author]
    assert data[author][novel2] == {}

    # Call the function with a new author and a new novel
    author2 = "Jane Doe"
    novel3 = "The Amazing Novel"
    book_logger.check_data_structure(data, author2, novel3)

    # Check if the structure has been updated with the new author and novel
    assert author2 in data
    assert novel3 in data[author2]
    assert data[author2][novel3] == {}


def test_is_file_empty():
    # Create a temporary file with some content
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write("This is some content.")

    # Test when the file is not empty
    assert book_logger.is_file_empty(temp_file.name) is False

    # Test when the file is empty
    empty_file_path = os.path.join(tempfile.gettempdir(), "empty_file.txt")
    with open(empty_file_path, 'w'):
        pass  # Creating an empty file

    assert book_logger.is_file_empty(empty_file_path) is True

    # Test when the file doesn't exist
    non_existent_file_path = "non_existent_file.txt"
    assert book_logger.is_file_empty(non_existent_file_path) is True

    # Clean up: delete the temporary files
    os.remove(temp_file.name)
    os.remove(empty_file_path)


def test_add_file_header():
    # Create temporary file paths for txt and csv
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as txt_file:
        txt_file_path = txt_file.name

    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as csv_file:
        csv_file_path = csv_file.name

    # Define header patterns
    txt_header_pattern = '{col1:40} | {col2:40} | {col3:20} | {col4:20}\n'
    csv_header_pattern = '"{col1}","{col2}","{col3}","{col4}"\n'

    # Test when boolean is True for txt file (indicating empty)
    boolean_true = True
    book_logger.add_file_header(boolean_true, txt_header_pattern, txt_file_path)

    # Check if the header has been added to the txt file with the correct pattern
    with open(txt_file_path, 'r') as f:
        content = f.read()
        expected_line_txt = txt_header_pattern.format(col1='Author/Authors',
                                                      col2='Book Title',
                                                      col3='Start Date',
                                                      col4='End Date')
        assert content.startswith(expected_line_txt)

    # Test when boolean is True for csv file (indicating empty)
    book_logger.add_file_header(boolean_true, csv_header_pattern, csv_file_path)

    # Check if the header has been added to the csv file with the correct pattern
    with open(csv_file_path, 'r') as f:
        content_csv = f.read()
        expected_line_csv = csv_header_pattern.format(col1='Author/Authors',
                                                      col2='Book Title',
                                                      col3='Start Date',
                                                      col4='End Date')
        assert content_csv.startswith(expected_line_csv)

    # Clean up: delete the temporary files
    os.remove(txt_file_path)
    os.remove(csv_file_path)


def test_check_start_date_user_wants_to_enter_start_date():
    data = {'author1': {'novel1': {}}, 'author2': {'novel2': {'Start Date': '2022-01-01'}}}
    author = 'author1'
    novel = 'novel1'

    with patch('builtins.input', return_value='Y'):
        result = book_logger.check_start_date(data, author, novel)

    assert result == 'Y'

    with patch('builtins.input', return_value='y'):
        result = book_logger.check_start_date(data, author, novel)

    assert result == 'Y'

    with patch('builtins.input', return_value='Yes'):
        result = book_logger.check_start_date(data, author, novel)

    assert result == 'Yes'

    with patch('builtins.input', return_value='yes'):
        result = book_logger.check_start_date(data, author, novel)

    assert result == 'Yes'


def test_check_start_date_user_does_not_want_to_enter_start_date():
    data = {'author1': {'novel1': {}}, 'author2': {'novel2': {}}}
    author = 'author2'
    novel = 'novel2'

    with patch('builtins.input', return_value='N'):
        result = book_logger.check_start_date(data, author, novel)

    assert result != ('Y' or 'y' or 'Yes' or 'yes')


def test_check_start_date_already_exists():
    data = {'author1': {'novel1': {'Start Date': '2022-01-01'}}, 'author2': {'novel2': {}}}
    author = 'author1'
    novel = 'novel1'

    result = book_logger.check_start_date(data, author, novel)

    assert result is None  # Since the start date already exists, the function should return None


def test_modify_entry_quit():
    data = {
        "example_key": {
            "nested_key": {"inner_key": "value"}
        }
    }

    result = "Quit"
    book_logger.modify_entry(data, result)

    # Assuming that 'Quit' should not modify the data
    assert data == {
        "example_key": {
            "nested_key": {"inner_key": "value"}
        }
    }


def test_modify_author_existing_author():
    data = {
        "existing_author": {
            "nested_key": {"inner_key": "value"}
        }
    }
    exit_commands = ["Exit", "exit"]

    # Simulate user input for an existing author
    input_values = ["existing_author", "replacement_author"]
    original_input = builtins.input

    def mock_input(prompt):
        return input_values.pop(0)

    builtins.input = mock_input

    book_logger.modify_author(data, exit_commands)

    # Reset the original input function
    builtins.input = original_input

    # Add assertions or checks here based on the expected behavior after modifying the author.
    assert "replacement_author" in data
    assert "existing_author" not in data


def test_modify_author_exit_command():
    data = {
        "existing_author": {
            "nested_key": {"inner_key": "value"}
        }
    }
    exit_commands = ["Exit", "exit"]

    # Simulate user input for an exit command
    input_values = ["Exit"]
    original_input = builtins.input

    def mock_input(prompt):
        return input_values.pop(0)

    builtins.input = mock_input

    book_logger.modify_author(data, exit_commands)

    # Reset the original input function
    builtins.input = original_input

    # Add assertions or checks here based on the expected behavior after receiving an exit command.
    # For example, data should remain unchanged.
    assert data == {
        "existing_author": {
            "nested_key": {"inner_key": "value"}
        }
    }


def test_modify_book_exit_command():
    data = {"author": {"novel": {"key": "value"}}}
    exit_commands = ["Exit", "exit"]

    with patch('builtins.input', side_effect=["Exit"]):
        book_logger.modify_book(data, exit_commands)

    assert data == {"author": {"novel": {"key": "value"}}}


def test_modify_book_valid_input():
    data = {"author": {"novel": {"key": "value"}}}
    exit_commands = ["Exit", "exit"]

    with patch('builtins.input', side_effect=["author", "novel", "replacement"]):
        book_logger.modify_book(data, exit_commands)

    assert data == {"author": {"replacement": {"key": "value"}}}


def test_modify_book_existing_book():
    data = {
        "existing_author": {
            "existing_book": {"inner_key": "value"}
        }
    }

    result = "Book"
    exit_commands = ["Exit", "exit"]

    # Simulate user input for an existing book
    input_values = ["existing_author", "existing_book", "replacement_book"]
    original_input = builtins.input

    def mock_input(prompt):
        return input_values.pop(0)

    builtins.input = mock_input

    book_logger.modify_entry(data, result)

    # Reset the original input function
    builtins.input = original_input

    # Add assertions or checks here based on the expected behavior after modifying the book.
    assert "replacement_book" in data["existing_author"]
    assert "existing_book" not in data["existing_author"]


sample_data = {
    "Author1": {
        "Book1": {"Start Date": "2022-01-01", "End Date": "2022-02-01"},
        "Book2": {"Start Date": "2022-03-01", "End Date": "2022-04-01"},
    },
    "Author2": {
        "Book3": {"Start Date": "2022-05-01", "End Date": "2022-06-01"},
        "Book4": {"Start Date": "2022-07-01", "End Date": "2022-08-01"},
    },
}

# Sample exit commands for testing
exit_commands = ["Exit", "exit"]


def test_import_JSON_PATH():
    # Get the directory of the test module
    test_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the directory of book-logger.py module
    module_dir = os.path.dirname(os.path.abspath(book_logger.__file__))

    assert book_logger.JSON_PATH == os.path.join(module_dir, book_logger.JSON_FILENAME)
    assert book_logger.JSON_PATH != os.path.join(test_dir, book_logger.JSON_FILENAME)


def test_import_existing_json():
    # Create a temporary file with some JSON data
    json_data = {"key": "value"}
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        json.dump(json_data, temp_file)

    # Set JSON_PATH to the temporary file
    book_logger.JSON_PATH = temp_file.name

    # Call the function and check if it returns the expected JSON data
    result = book_logger.import_json()
    assert result == json_data

    # Clean up: delete the temporary file
    os.remove(temp_file.name)


def test_import_nonexistent_json():
    # Set JSON_PATH to a non-existent file
    book_logger.JSON_PATH = "nonexistent_file.json"

    # Call the function and check if it returns an empty dictionary
    result = book_logger.import_json()
    assert result == {}


if __name__ == "__main__":
    main()
