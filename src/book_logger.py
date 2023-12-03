import random
import os
import datetime
import json
from typing import Dict


# Get the user's home directory
HOME_DIRECTORY = os.path.expanduser('~')

# Create a "Documents" directory path within the home directory
DOCUMENTS_DIRECTORY = os.path.join(HOME_DIRECTORY, "Documents")

CELL_1 = "Author/Authors"
CELL_2 = "Book Title"
CELL_3 = "Start Date"
CELL_4 = "End Date"

TXT_FILENAME = "book-log.txt"
TXT_PATH = os.path.join(DOCUMENTS_DIRECTORY, TXT_FILENAME)
TXT_FILE_LINE = '{col1:40} | {col2:40} | {col3:20} | {col4:20}\n'

CSV_FILENAME = "book-log.csv"
CSV_PATH = os.path.join(DOCUMENTS_DIRECTORY, CSV_FILENAME)
CSV_FILE_LINE = '"{col1}","{col2}","{col3}","{col4}"\n'

JSON_FILENAME = "book-log.json"
JSON_PATH = os.path.join(os.path.dirname(__file__), JSON_FILENAME)


def main():
    display_random_quote()
    program_data = import_json()

    program_options = """
Book Log Options:

Start - Add start date for new book
End - Add end date for new or existing book
View Log - Display book log entries
Modify Entry - Edit author(s), book title, start/end date
Push - Writes data to files if it was previously unable to due to it being open in other program
Quit - Terminates program

>>> """
    user_input = input(program_options).strip().lower().title()

    while user_input != "Quit":
        if user_input == "Start":
            start_entry(program_data)
            dump_to_files(program_data)
        elif user_input == "End":
            end_entry(program_data)
            dump_to_files(program_data)
        elif user_input == "View Log":
            print()
            display_txt_file()
        elif user_input == "Modify Entry":
            option_choice = display_modifier_options()
            modify_entry(program_data, option_choice)
            if option_choice not in ["Quit", "Q"]:
                dump_to_files(program_data)
        elif user_input == "Push":
            dump_to_files(program_data)
        else:
            print("Unknown command, please try again.")

        print()
        user_input = input(program_options[19:]).strip().lower().title()


def display_random_quote():
    welcome_messages = [
        "Hola!\n",
        "Thanks for using the program!\n",
        "Live, Laugh, Love.\n",
        "The world is your oyster.\n",
        '"My mother always used to say: The older you get, the better you get, unless you\'re a banana." - Rose \
(Betty White), The Golden Girls\n',
        '"Before you criticize someone, you should walk a mile in their shoes. That way when you criticize them, you \
are a mile away from them and you have their shoes." - Jack Handey\n',
        '"Never follow anyone else\'s path. Unless you\'re in the woods and you\'re lost and you see a path. Then by \
all means follow that path." - Ellen Degeneres\n',
        '"Insomnia sharpens your math skills because you spend all night calculating how much sleep you\'ll get if \
you\'re able to `fall asleep right now.`" - Anonymous\n',
        '"I\'m not superstitious, but I am a little stitious." - Michael Scott (Steve Carrell), The Office\n',
        '"If Jesus can walk on water, can he swim on land?" - Bo Burnham\n',
        '"I walk around like everything\'s fine, but deep down, inside my shoe, my sock is sliding off." - Anonymous\n',
        '"There is no sunrise so beautiful that it is worth waking me up to see it." - Mindy Kaling, Is Everyone \
Hanging Out Without Me?\n',
        '"Truth hurts. Maybe not as much as jumping on a bicycle with a seat missing, but it hurts." - Lt. Frank \
Drebin (Leslie Nielsen), Naked Gun 2 1/2: The Smell of Fear\n',
        '"Bread makes you fat?!" - Scott Pilgrim (Michael Cera), Scott Pilgrim vs. the World\n',
        '"I did college, majored in smart." - Jon Mess\n',
        '"I spilled my beans \'cause I\'m a fiend, I lost my extra mustard." - Jon Mess\n',
        '"My mama says that alligators are ornery because they got all them teeth and no toothbrush." - Bobby Boucher \
(Adam Sandler), The Waterboy\n',
        '"She\'s a referee, and I\'m lethally overdosed on pumpkin pie." - Jon Mess\n'
    ]
    message = random.choice(welcome_messages)
    print(message)


def import_json() -> dict:
    """
    Imports json data if any exists, otherwise creates an empty dict
    :return: Either json data or new dict
    """
    try:
        file = open(JSON_PATH, "r")
    except FileNotFoundError:
        print("No data available currently to import, this should change once book log begins.\n")
        data_dict = {}
        return data_dict
    else:
        with file:
            data_dict = json.load(file)
        print("Importing existing data from book-log.json.\n")
        return data_dict


def start_entry(data: Dict[str, Dict[str, Dict[str, str]]]) -> None:
    """
    Creates new log entry with timestamp of start date
    :param data: Book logger data (dict, nested 3 levels)
    :return: None
    """
    name = input("Enter name(s) of author/authors. >>> ").strip()
    book = input("Enter title of book. >>> ").strip()
    check_data_structure(data, name, book)
    date1 = timestamp()
    date2 = "N/A"
    data[name][book]["Start Date"] = date1
    data[name][book]["End Date"] = date2

    add_file_header(is_file_empty(TXT_PATH), TXT_FILE_LINE, TXT_PATH)
    with open(TXT_PATH, "a") as file:
        file.write(TXT_FILE_LINE.format(col1=name, col2=book, col3=date1, col4=date2))

    try:
        add_file_header(is_file_empty(CSV_PATH), CSV_FILE_LINE, CSV_PATH)
    except PermissionError:
        print("Unable to write new data to csv file, please close the program the file is opened in and try again.")
        print("(You can use the 'Push' command to write all data back to file once the program is closed)")
    else:
        try:
            with open(CSV_PATH, "a") as file:
                file.write(CSV_FILE_LINE.format(col1=name, col2=book, col3=date1, col4=date2))
        except PermissionError:
            print("Data has been saved.")

    with open(JSON_PATH, "w") as file:
        json.dump(data, file, indent=4)


def check_data_structure(data: Dict[str, Dict[str, Dict[str, str]]], author: str, novel: str):
    """
    Checks if there's already a nested layer matching the second and third parameter.
    :param data: Book logger data (dict, nested 3 levels)
    :param author: Second layer of nesting
    :param novel: Third layer of nesting
    :return: None
    """
    if author not in data:
        data[author] = {}

    if novel not in data[author]:
        data[author][novel] = {}


def timestamp() -> str:
    """
    Grabs system date and time; converts the date to an American format and formats the time to show only hours,
    minutes, and seconds.
    :return: str
    """
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime("%m/%d/%Y %H:%M:%S")


def add_file_header(boolean: bool, header_pattern: str, path: str):
    """
    If the boolean variable is set to True (indicating the file doesn't have content / empty = True), headers will be
    created to display what each section of file represents.
    :param boolean:
    :param header_pattern: Str to format in pattern specific to type of file (txt, csv, etc.)
    :param path: File path to write headers
    :return: None
    """
    if boolean:
        with open(path, "w") as f:
            f.write(header_pattern.format(
                col1=CELL_1, col2=CELL_2, col3=CELL_3, col4=CELL_4))


def is_file_empty(file_path: str) -> bool:
    """
    Returns True if the file path doesn't exist, otherwise the bool of os.path.getsize(file_path) == 0.
    :param file_path: Path to file (str)
    :return: bool
    """
    if not os.path.exists(file_path):
        return True

    return os.path.getsize(file_path) == 0


def end_entry(data: Dict[str, Dict[str, Dict[str, str]]]) -> None:
    """
    Adds and end date to book log
    :param data: Book logger data (dict, nested 3 levels)
    :return: None
    """
    name = input("Enter name(s) of author/authors. >>> ").strip()
    book = input("Enter title of book. >>> ").strip()
    check_data_structure(data, name, book)
    date2 = timestamp()
    result = check_start_date(data, name, book)
    set_start_date(data, result, name, book)
    data[name][book]["End Date"] = date2


def check_start_date(data: Dict[str, Dict[str, Dict[str, str]]], author: str, novel: str) -> str:
    """
    Asks user if they would like to add a start date if one hasn't been found
    :param data: Book logger data (dict, nested 3 levels)
    :param author: Second level of nesting
    :param novel: Third level of nesting
    :return: User answer (str, only if no start date found)
    """
    if "Start Date" not in data[author][novel]:
        answer = input("No start date was found, would you like to enter one? Y/N >>> ").strip().lower().capitalize()
        return answer


def set_start_date(data: Dict[str, Dict[str, Dict[str, str]]], answer: str, author: str, novel: str):
    """

    :param data: Book logger data (dict, nested 3 levels)
    :param answer: str, 'Yes' or 'Y' prompts user for new start date, otherwise puts a placeholder if one isn't found
    :param author: Second level of nesting
    :param novel: Third level of nesting
    :return: None
    """
    if (answer == "Y") or (answer == "Yes"):
        data[author][novel]["Start Date"] = input("Enter new date: >>> ").strip()

    elif ("Start Date" not in data[author][novel]) and ((answer != "Y") or (answer != "Yes")):
        data[author][novel]["Start Date"] = 'N/A'


def display_txt_file():
    try:
        file = open(TXT_PATH, "r")
    except FileNotFoundError:
        print("No book-log.txt file found, please add entries before using this command.\n")
    else:
        with file:
            for line in file:
                print(line.rstrip())


def display_modifier_options() -> str:
    prompt = ("Which field would you like to modify?\n\n"
              "Author/Authors : A\n"
              "Book Title : B\n"
              "Start Date : S\n"
              "End Date : E\n"
              "Back (Back to Main Menu)\n\n"
              ">>> ")
    result = input(prompt).strip().lower().title()
    return result


def modify_entry(data: Dict[str, Dict[str, Dict[str, str]]], result: str) -> None:
    """
    Gathers needed information for modifying structure of data
    :param data: Book logger data (dict, nested 3 levels)
    :param result: str, goes back to main menu if 'Quit' or 'Q', otherwise it should reflect which data entry to modify.
    :return: None
    """
    sentinels = ["Exit", "exit"]

    if result == "Back":
        return

    elif (result == "Author") or (result == "Authors") or (result == "A"):
        modify_author(data, sentinels)

    elif (result == "Book") or (result == "Book Title") or (result == "B"):
        modify_book(data, sentinels)

    elif (result == "Start") or (result == "Start Date") or (result == "S"):
        modify_start_date(data, sentinels)

    elif (result == "End") or (result == "End Date") or (result == "E"):
        modify_end_date(data, sentinels)

    else:
        print("Invalid, try again.")


def modify_author(data: Dict[str, Dict[str, Dict[str, str]]], exit_commands: list[str]):
    while True:
        author = input("Enter name(s) of author/authors to modify. >>> ")
        if author in exit_commands:
            return  # Nothing else needed to execute

        if author in data:
            break  # Valid author name provided, exit the loop

        else:
            print("Entry with author/authors not found within any fields. Please enter existing field data or type \
    'Exit'.")
            print("Enter 'Exit', then 'Quit' or 'Q' and use 'View Log' to copy and paste exact values.")
            print("(Not case-sensitive)\n")

    # Only executes if the user would like to continue with attempting to modify data
    replacement = input("What would you like to replace it with? >>> ")
    data[replacement] = data.pop(author)
    print("Author/authors has been replaced with:", replacement)


def modify_book(data: Dict[str, Dict[str, Dict[str, str]]], exit_commands: list[str]):
    while True:
        author = input("Enter name(s) of author/authors book is associated with. >>> ")
        if author in exit_commands:
            return

        novel = input("Enter title of book to modify. >>> ")
        if novel in exit_commands:
            return

        if (author not in data) or (novel not in data[author]):
            print("Book and/or author/authors not found in data. Please enter existing field data or type 'Exit'.")
            print("Enter 'Exit', then 'Quit' or 'Q' and use 'View Log' to copy and paste exact values.")
            print("(Not case-sensitive)\n")

        else:
            break

    replacement = input("What would you like to replace it with? >>> ")
    data[author][replacement] = data[author].pop(novel)
    print("Book has been replaced with:", replacement)


def modify_start_date(data: Dict[str, Dict[str, Dict[str, str]]], exit_commands: list[str]):
    while True:
        author = input("Enter name(s) of author/authors book is associated with. >>> ")
        if author in exit_commands:
            return

        novel = input("Enter title of book date is associated with. >>> ")
        if novel in exit_commands:
            return

        start_date = input("Enter start date to modify. >>> ")
        if start_date in exit_commands:
            return

        if (author not in data) or (novel not in data[author]) or (
                start_date not in data[author][novel]["Start Date"]):
            print("One of the entered values were incorrect. Please enter existing field data or type 'Exit'.")
            print("Enter 'Exit', then 'Quit' or 'Q' and use 'View Log' to copy and paste exact values.")
            print("(Not case-sensitive)\n")

        else:
            break

    replacement = input("What would you like to replace it with? >>> ")
    data[author][novel]["Start Date"] = replacement
    print("Start date has been replaced with:", replacement)


def modify_end_date(data: Dict[str, Dict[str, Dict[str, str]]], exit_commands: list[str]):
    while True:
        author = input("Enter name(s) of author/authors book is associated with. >>> ")
        if author in exit_commands:
            return

        novel = input("Enter title of book date is associated with. >>> ")
        if novel in exit_commands:
            return

        end_date = input("Enter end date to modify. >>> ")
        if end_date in exit_commands:
            return

        if (author not in data) or (novel not in data[author]) or (
                end_date not in data[author][novel]["End Date"]):
            print("One of the entered values were incorrect. Please enter existing field data or type 'Exit'.")
            print("Enter 'Exit', then 'Quit' or 'Q' and use 'View Log' to copy and paste exact values.")
            print("(Not case-sensitive)\n")

        else:
            break

    replacement = input("What would you like to replace it with? >>> ")
    data[author][novel]["End Date"] = replacement
    print("End date has been replaced with:", replacement)


def dump_to_files(data: Dict[str, Dict[str, Dict[str, str]]]) -> None:
    with open(TXT_PATH, "w") as file:
        file.write(TXT_FILE_LINE.format(
            col1=CELL_1, col2=CELL_2, col3=CELL_3, col4=CELL_4))
        for name, books in data.items():
            for book, dates in books.items():
                date1 = dates.get("Start Date", "N/A")
                date2 = dates.get("End Date", "N/A")
                file.write(f"{name:40} | {book:40} | {date1:20} | {date2:20}\n")

    try:
        file = open(CSV_PATH, "w")
    except PermissionError:
        print("Unable to write new data to csv file, close other program and run this command again.")
        print("(You can use the 'Push' command to write all data back to file once the program is closed)")
    else:
        with file:
            file.write(CSV_FILE_LINE.format(
                col1=CELL_1, col2=CELL_2, col3=CELL_3, col4=CELL_4))
            for name, books in data.items():
                for book, dates in books.items():
                    date1 = dates.get("Start Date", "N/A")
                    date2 = dates.get("End Date", "N/A")
                    file.write(f'"{name}","{book}",{date1},{date2}\n')

    with open(JSON_PATH, "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    main()
