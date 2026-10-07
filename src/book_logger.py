import random
import os
import datetime
import json
from configparser import ConfigParser
from typing import Dict


# Get the user's home directory
HOME_DIRECTORY = os.path.normpath(os.path.expanduser('~'))

# Create a "Documents" directory path within the home directory
DOCUMENTS_DIRECTORY = os.path.join(HOME_DIRECTORY, "Documents")

CELL_1 = "Author/Authors"
CELL_2 = "Book Title"
CELL_3 = "Start Date"
CELL_4 = "End Date"
# TODO: will need to move below variable and CSV equivalent to main after 
# implementing option to change file name
TXT_FILENAME = "book-log.txt"
DEFAULT_TXT_PATH = os.path.join(DOCUMENTS_DIRECTORY, TXT_FILENAME)
TXT_FILE_LINE = '{col1:40} | {col2:40} | {col3:20} | {col4:20}\n'

CSV_FILENAME = "book-log.csv"
DEFAULT_CSV_PATH = os.path.join(DOCUMENTS_DIRECTORY, CSV_FILENAME)
CSV_FILE_LINE = '"{col1}","{col2}","{col3}","{col4}"\n'

JSON_FILENAME = "book-log.json"
JSON_PATH = os.path.join(os.path.dirname(__file__), JSON_FILENAME)

INI_FILENAME = "settings.ini"
INI_PATH = os.path.join(os.path.dirname(__file__), INI_FILENAME)

sentinels = ["quit", "Quit", "q", "Q", "exit", "Exit", "e", "E"]

def main():
    display_random_quote()
    program_data = import_json()
    program_settings = import_ini()
    
    program_options = """
Book Log Options:

Start - Add start date for new book
Finish - Add end date for new or existing book
View Log - Display book log entries
Modify Entry - Edit author(s), book title, start/end date
Push - Writes data to files if it was previously unable to due to it being open\
 in other program
Settings - View and edit program settings
Quit - Terminates program

>>> """
    user_input = input(program_options).strip().lower().title()

    while user_input not in sentinels:
        # TODO make sure pathing works right
        active_txt_path = program_settings["text_file_path"]
        active_csv_path = program_settings["csv_file_path"]
        has_changed = False
        # TODO only dump_to_files for start/end entry if has_changed
        if user_input == "Start":
            start_entry(program_data, active_txt_path, active_csv_path)
            dump_to_files(program_data, active_txt_path, active_csv_path)
        elif user_input == "Finish":
            end_entry(program_data)
            dump_to_files(program_data, active_txt_path, active_csv_path)
        elif user_input == "View Log":
            print()
            display_txt_file(active_txt_path)
        elif user_input == "Modify Entry":
            option_choice = display_modifier_options()
            has_changed = modify_entry(program_data, option_choice)
            if option_choice not in sentinels and has_changed == True: # Because the modify_entry() function returns after an invalid input, both conditions are needed.
                dump_to_files(program_data, active_txt_path, active_csv_path)
        elif user_input == "Push":
            dump_to_files(program_data, active_txt_path, active_csv_path)
        elif user_input == "Settings":
            # TODO implement settings logic here
            option_choice = display_settings_options(program_settings)
            has_changed = change_settings(program_settings, option_choice)
            program_settings = import_ini() # Refresh program_settings
            # TODO ensure has_changed is calculated correctly and txt_path/csv_path are updated before dump_to_files executes
            if option_choice not in sentinels and has_changed == True:
                active_txt_path = program_settings['text_file_path']
                active_csv_path = program_settings['csv_file_path']
                dump_to_files(program_data, active_txt_path, active_csv_path)
        else:
            print("Unknown command, please try again.")

        #print()
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
    

def import_ini() -> dict:
    try:
        file = open(INI_PATH, 'r')
    except FileNotFoundError:
        print(f"No settings available to import, {INI_FILENAME} will be " \
        "created and populated with default settings.")
        config = ConfigParser()
        config['DEFAULT'] = {'text_file_path': DEFAULT_TXT_PATH,
                             'csv_file_path': DEFAULT_CSV_PATH,
                             'message_type': 'quotes',
                             'repeat_menu': 'Yes'}
        with open(INI_PATH, 'w') as file:
            config.write(file)
        settings_dict = {}
        settings_dict['text_file_path'] = config['DEFAULT']['text_file_path']
        settings_dict['csv_file_path'] = config['DEFAULT']['csv_file_path']
        settings_dict['message_type'] = config['DEFAULT']['message_type']
        settings_dict['repeat_menu'] = config['DEFAULT'].getboolean(
            'repeat_menu')
        return settings_dict
    else:
        settings_dict = safe_import()
        return settings_dict


def safe_import():
    # TODO Add more error checking/sanitize setting.ini input
    config = ConfigParser()
    config.read(INI_PATH)
    needs_save = False
        
    print(f"Loading settings from {INI_FILENAME}.")

    # Process text path
    raw_text_path = config.get('DEFAULT', 'text_file_path', fallback=DEFAULT_TXT_PATH).strip()
    text_file_path = validate_path(raw_text_path, TXT_FILENAME, DEFAULT_TXT_PATH)
    if text_file_path != raw_text_path:
        config['DEFAULT']['text_file_path'] = text_file_path
        needs_save = True

    # Process csv path
    raw_csv_path = config.get('DEFAULT', 'csv_file_path', fallback=DEFAULT_CSV_PATH).strip()
    csv_file_path = validate_path(raw_csv_path, CSV_FILENAME, DEFAULT_CSV_PATH)
    if csv_file_path != raw_csv_path:
        config['DEFAULT']['csv_file_path'] = csv_file_path
        needs_save = True

    message_type = config.get('DEFAULT', 'message_type', fallback='quotes')
    if message_type not in ['quotes', 'verses', 'both', 'none']:
        message_type = 'quotes'
        config['DEFAULT']['message_type'] = 'quotes'
        needs_save = True

    try:
        repeat_menu = config['DEFAULT'].getboolean('repeat_menu', True)
    except ValueError:
        print(f"\n'repeat_menu' within 'settings.ini' is set to invalid value.")
        print(f"Changing value to default value True.")
        print('Use "Settings" command to see more info on changing settings.')
        repeat_menu = True
        config['DEFAULT']['repeat_menu'] = 'True'
        needs_save = True

    # If any paths had to be repaired to defaults, overwrite settings.ini immediately
    if needs_save:
        with open(INI_PATH, 'w') as file:
            config.write(file)

    return {
        'text_file_path': text_file_path,
        'csv_file_path': csv_file_path,
        'message_type': message_type,
        'repeat_menu': repeat_menu
    }


def validate_path(path: str, target_filename: str, default_path: str) -> str: # TODO update/revise doc string
    """
    Validates the path. If the path is a directory or lacks a file extension, 
    the target_filename is appended automatically. 
    Rejects paths that specify a mismatched filename. Creates necessary parent directories.
    """
    # Split on both slashes and discard empty components caused by duplicates
    parts = [p for p in path.replace('\\', '/').split('/') if p]

    # 1. Reconstruct path safely with native OS separators
    clean_path = os.sep.join(parts)
    if path.startswith('/') or path.startswith('\\'):
        clean_path = os.sep + clean_path
    absolute_path = os.path.normpath(os.path.abspath(clean_path))

    # 2. Cross-platform check if absolute_path is inside HOME_DIRECTORY
    try:
        # commonpath returns the longest common sub-path
        common = os.path.commonpath([absolute_path, HOME_DIRECTORY])
        # On Windows, lower() handles 'C:\' vs 'c:\' case differences
        if common.lower() != HOME_DIRECTORY.lower():
            print("Directories outside of current user's directory are currently unsupported.")
            return default_path
    except ValueError:
        # Triggers on Windows if paths are on different drive letters (e.g. C: vs D:)
        print("Directories outside of current user's directory are currently unsupported.")
        return default_path

    # 3. Extension & Directory handling
    if os.path.isdir(absolute_path):
        absolute_path = os.path.join(absolute_path, target_filename)
    else:
        # Check if the path targets a file or a folder by looking for an extension
        _, ext = os.path.splitext(absolute_path)

        if ext:
            # The user provided a file extension. Extract the filename and verify it matches.
            user_filename = os.path.basename(absolute_path)
            if user_filename != target_filename:
                print(f"Invalid filename: Expected '{target_filename}' or a directory path, but got '{user_filename}' instead.")
                print(f"Setting path to '{default_path}'.")
                return default_path
        else:
            # No extension provided, assume it's a new directory path and append the target
            absolute_path = os.path.join(absolute_path, target_filename)

    # 4. Create directory safely (mode=0o755 is ignored on Windows, so it won't crash)
    dir_to_make = os.path.dirname(absolute_path)

    try:
        if dir_to_make:
            os.makedirs(dir_to_make, mode=0o755, exist_ok=True)
        return absolute_path
    except (OSError, PermissionError) as e:
        print(f"Failed to create path due to a system error: {e}")
        return default_path


def start_entry(data: Dict[str, Dict[str, Dict[str, str]]], txt_path:str, csv_path:str) -> None: # TODO fix nested try/except block
    """
    Creates new log entry with timestamp of start date
    :param data: Book logger data (dict, nested 3 levels)
    :return: None
    """
    name = input("Enter name(s) of author/authors. >>> ").strip()
    if name in sentinels:
        return
    
    book = input("Enter title of book. >>> ").strip()
    if book in sentinels:
        return
    
    check_data_structure(data, name, book)
    date1 = timestamp()
    date2 = "N/A"
    data[name][book]["Start Date"] = date1
    data[name][book]["End Date"] = date2

    add_file_header(is_file_empty(txt_path), TXT_FILE_LINE, txt_path)
    with open(txt_path, "a") as file:
        file.write(TXT_FILE_LINE.format(col1=name, col2=book, col3=date1, col4=date2))

    try:
        add_file_header(is_file_empty(csv_path), CSV_FILE_LINE, csv_path)
    except PermissionError:
        print("Unable to write new data to csv file, please close the program the file is opened in and try again.")
        print("(You can use the 'Push' command to write all data back to file once the program is closed)")
    else:
        try:
            with open(csv_path, "a") as file:
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
    if name in sentinels:
        return
    
    book = input("Enter title of book. >>> ").strip()
    if book in sentinels:
        return
    
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
    
    return data[author][novel]['Start Date']


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


def display_txt_file(txt_path:str) -> None:
    try:
        file = open(txt_path, "r")
    except FileNotFoundError:
        print("No book-log.txt file found, please add entries before using this command.\n")
    else:
        with file:
            for line in file:
                print(line.rstrip())


def display_modifier_options() -> str:
    prompt = ("\nWhich field would you like to modify?\n\n"
              "Author/Authors : A\n"
              "Book Title : B\n"
              "Start Date : S\n"
              "Finish Date : F\n"
              "Back (Back to Main Menu)\n\n"
              ">>> ")
    result = input(prompt).strip().lower().title()
    return result


def display_settings_options(settings_dict) -> str:
    print()
    print(f"Saving '{TXT_FILENAME}' to '{settings_dict.get('text_file_path')}'")
    print(f"Saving '{CSV_FILENAME}' to '{settings_dict.get('csv_file_path')}'")
    print(f"Random quotes set to '{settings_dict.get('message_type')}'")
    print(f"Repeat options set to '{settings_dict.get('repeat_menu')}'")

    prompt = ("\nWhich option would you like to change?\n\n"
              "Text File Path - The directory where '{TXT_FILENAME}' is saved\n"
              "CSV File Path - The directory where '{CSV_FILENAME}' is saved\n"
              "Quotes - Type of quotes displayed (default/verses/both/none)\n"
              "Repeat - Toggle displaying menu options after every command\n\n"
              ">>> ")
    result = input(prompt).strip().lower()
    return result


def modify_entry(data: Dict[str, Dict[str, Dict[str, str]]], result: str) -> bool:
    """
    Gathers needed information for modifying structure of data
    :param data: Book logger data (dict, nested 3 levels)
    :param result: str, goes back to main menu if it matches a sentinel value, 
    otherwise it should reflect which data entry to modify.
    :return: bool, if any changes occurred, returns True
    """
    if (result == "Back") or (result in sentinels):
        return False

    elif (result == "Author") or (result == "Authors") or (result == "A"):
        has_changed = modify_author(data, sentinels)
        return has_changed

    elif (result == "Book") or (result == "Book Title") or (result == "B"):
        has_changed = modify_book(data, sentinels)
        return has_changed

    elif (result == "Start") or (result == "Start Date") or (result == "S"):
        has_changed = modify_start_date(data, sentinels)
        return has_changed

    elif (result == "Finish") or (result == "Finish Date") or (result == "F"):
        has_changed = modify_end_date(data, sentinels)
        return has_changed

    else:
        print("Invalid, try again.")
        return False


def modify_author(data: Dict[str, Dict[str, Dict[str, str]]], exit_commands: list[str]) -> bool:
    """
    Responsible for editing author values within an entry
    :param data: Book logger data (dict, nested 3 levels)
    :param exit_commands: A global list of various sentinel values that can be used to undo or change mind over what to do
    :return: bool, if any changes occurred, returns True
    """
    while True:
        author = input("Enter name(s) of author/authors to modify. >>> ")
        if author in exit_commands:
            return False # Nothing else needed to execute

        if author in data:
            break  # Valid author name provided, exit the loop

        else:
            print("Entry with author/authors not found within any fields. Please enter existing field data or type \
'Exit'.")
            print("Enter 'Exit', then use 'View Log' to copy and paste exact values.")
            print("(Not case-sensitive)\n")

    # Only executes if the user would like to continue with attempting to modify data
    replacement = input("What would you like to replace it with? >>> ")
    data[replacement] = data.pop(author)
    print("Author/authors has been replaced with:", replacement)
    has_changed = True
    return has_changed


def modify_book(data: Dict[str, Dict[str, Dict[str, str]]], exit_commands: list[str]) -> bool:
    """
    Responsible for editing book title values within an entry
    :param data: Book logger data (dict, nested 3 levels)
    :param exit_commands: A global list of various sentinel values that can be used to undo or change mind over what to do
    :return: bool, if any changes occurred, returns True
    """
    while True:
        author = input("Enter name(s) of author/authors book is associated with. >>> ")
        if author in exit_commands:
            return False

        novel = input("Enter title of book to modify. >>> ")
        if novel in exit_commands:
            return False

        if (author not in data) or (novel not in data[author]):
            print("Book and/or author/authors not found in data. Please enter existing field data or type 'Exit'.")
            print("Enter 'Exit', then use 'View Log' to copy and paste exact values.")
            print("(Not case-sensitive)\n")

        else:
            break

    replacement = input("What would you like to replace it with? >>> ")
    data[author][replacement] = data[author].pop(novel)
    print("Book has been replaced with:", replacement)
    has_changed = True
    return has_changed


def modify_start_date(data: Dict[str, Dict[str, Dict[str, str]]], exit_commands: list[str]) -> bool:
    """
    Responsible for editing the start date of an entry
    :param data: Book logger data (dict, nested 3 levels)
    :param exit_commands: A global list of various sentinel values that can be used to undo or change mind over what to do
    :return: bool, if any changes occurred, returns True
    """
    while True:
        author = input("Enter name(s) of author/authors book is associated with. >>> ")
        if author in exit_commands:
            return False

        novel = input("Enter title of book date is associated with. >>> ")
        if novel in exit_commands:
            return False

        start_date = input("Enter start date to modify. >>> ")
        if start_date in exit_commands:
            return False

        if (author not in data) or (novel not in data[author]) or (
                start_date not in data[author][novel]["Start Date"]):
            print("One of the entered values were incorrect. Please enter existing field data or type 'Exit'.")
            print("Enter 'Exit', then use 'View Log' to copy and paste exact values.")
            print("(Not case-sensitive)\n")

        else:
            break

    replacement = input("What would you like to replace it with? >>> ")
    data[author][novel]["Start Date"] = replacement
    print("Start date has been replaced with:", replacement)
    has_changed = True
    return has_changed


def modify_end_date(data: Dict[str, Dict[str, Dict[str, str]]], exit_commands: list[str]):
    """
    Responsible for editing the end date of an entry
    :param data: Book logger data (dict, nested 3 levels)
    :param exit_commands: A global list of various sentinel values that can be used to undo or change mind over what to do
    :return: bool, if any changes occurred, returns True
    """
    while True:
        author = input("Enter name(s) of author/authors book is associated with. >>> ")
        if author in exit_commands:
            return False

        novel = input("Enter title of book date is associated with. >>> ")
        if novel in exit_commands:
            return False

        end_date = input("Enter end date to modify. >>> ")
        if end_date in exit_commands:
            return False

        if (author not in data) or (novel not in data[author]) or (
                end_date not in data[author][novel]["End Date"]):
            print("One of the entered values were incorrect. Please enter existing field data or type 'Exit'.")
            print("Enter 'Exit', then and use 'View Log' to copy and paste exact values.")
            print("(Not case-sensitive)\n")

        else:
            break

    replacement = input("What would you like to replace it with? >>> ")
    data[author][novel]["End Date"] = replacement
    print("End date has been replaced with:", replacement)
    has_changed = True
    return has_changed


def dump_to_files(data: Dict[str, Dict[str, Dict[str, str]]], txt_path: str, csv_path: str) -> None:
    with open(txt_path, "w") as file:
        file.write(TXT_FILE_LINE.format(
            col1=CELL_1, col2=CELL_2, col3=CELL_3, col4=CELL_4))
        for name, books in data.items():
            for book, dates in books.items():
                date1 = dates.get("Start Date", "N/A")
                date2 = dates.get("End Date", "N/A")
                file.write(f"{name:40} | {book:40} | {date1:20} | {date2:20}\n")

    try:
        file = open(csv_path, "w")
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


def change_settings(settings_dict, result): # TODO finish implementing
    if (result in ['back', 'Back', 'b', 'B']) or (result in sentinels):
        return False
    elif (result == "text file path") or (result == "text") or (result == "t"):
        has_changed = change_file_path(TXT_FILENAME, settings_dict)
        return has_changed
    elif (result == "csv file path") or (result == "csv") or (result == "c"):
        has_changed = change_file_path(CSV_FILENAME, settings_dict)
        return has_changed
    elif (result == "quotes") or (result == "q"):
        has_changed = change_quotes # TODO finish implementation
        return has_changed
    elif (result == "repeat") or (result == "r"):
        has_changed = change_command_recap() # TODO finish implementation
        return has_changed
    else:
        print("Unknown command, please try again.")
        return False


def change_file_path(filename, settings_dict) -> bool: # 'filename' is TXT_FILENAME or CSV_FILENAME
    new_path = input("What would you like to change path to? ") 
    if (new_path in ['back', 'b']) or (new_path in sentinels):
        return False 

    # 1. Look up the correct default based on which file is being altered
    default_path = DEFAULT_TXT_PATH if filename == TXT_FILENAME else DEFAULT_CSV_PATH
    
    # 2. Validate, passing the default_path
    final_path = validate_path(new_path, filename, default_path)
    
    try:
        with open(final_path, 'a'):
            os.utime(final_path, None)
    except OSError as e:
        print(f"Could not initialize file: {e}")
        return False

    # 3. Save settings
    _, file_type = os.path.splitext(filename)
    config = ConfigParser()
    config['DEFAULT'] = settings_dict
    has_changed = assign_file_path(file_type, final_path, config)
    return has_changed


def assign_file_path(file_type, path, config) -> bool:
    if file_type == '.txt':
        config['DEFAULT']['text_file_path'] = path
        # TODO make some sort of lambda func to condense if/elif branches?
        with open(INI_PATH, 'w') as file:
            config.write(file)
        return True
    elif file_type == '.csv':
        config['DEFAULT']['csv_file_path'] = path
        with open(INI_PATH, 'w') as file:
            config.write(file)
        return True
    else:
        print(f"Unsupported file type used: {file_type}")
        return False


def change_quotes():
    raise NotImplementedError('Logic for changing type of quotes and frequency'
                              ' has not been implemented yet.')


def change_command_recap():
    raise NotImplementedError('Logic for how commands are displayed hasn\'t'
                              ' been implemented yet.')


if __name__ == "__main__":
    main()
