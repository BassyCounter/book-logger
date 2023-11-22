import random
import os
import datetime
import json


# todo type annotate stuff (purely just to get familiar with and hopefully increase productivity)
# todo update try/except blocks
def check_data_structure(data, author, novel):
    """ Creates dictionaries for any of the parameters that don't already exist. """
    if author not in data:
        data[author] = {}

    if novel not in data[author]:
        data[author][novel] = {}


def timestamp():
    """
    Grabs current date and time; converts the date to an American format and formats the time to show only hours,
    minutes, and seconds.
    """
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime("%m/%d/%Y %H:%M:%S")


def is_file_empty(file_path):
    """
    Returns True if the file path doesn't exist, otherwise it returns a boolean value of the specified expression.
    """
    if not os.path.exists(file_path):
        return True

    return os.path.getsize(file_path) == 0


def add_file_header(boolean, f_string, path):
    """
    If the boolean variable is set to True (indicating the file doesn't have content / empty = True), headers will be
    created to display what each section of file represents.
    """
    if boolean:
        with open(path, 'wt') as f:
            f.write(f_string.format(
                col1=cell1, col2=cell2, col3=cell3, col4=cell4))


def start_date_check(data, author, novel):
    """ Asks user if they would like to add a start date if one doesn't already exist """
    check_data_structure(data, author, novel)
    if "Start Date" not in data[author][novel]:
        answer = input("No start date was found, would you like to enter one? Y/N >>> ").strip().lower().capitalize()
        return answer


def modify_start_date(data, answer, author, novel):
    """
    Allows user to set a value for start date if the user puts Yes or Y as answer, otherwise sets it to N/A as long as
    it doesn't already exist
    """
    if (answer == "Y") or (answer == "Yes"):
        data[author][novel]["Start Date"] = input("Enter new date: >>> ").strip()

    elif ("Start Date" not in data[author][novel]) and ((answer != "Y") or (answer != "Yes")):
        data[author][novel]["Start Date"] = 'N/A'


def modify_entry(data, result):
    sentinels = ["Exit", "exit"]

    if (result == "Quit") or (result == "Q"):
        return

    elif (result == "Author") or (result == "Authors") or (result == "A"):
        while True:
            author = input("Enter name(s) of author/authors to modify. >>> ")
            if author in sentinels:
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

    elif (result == "Book") or (result == "Book Title") or (result == "B"):
        while True:
            author = input("Enter name(s) of author/authors book is associated with. >>> ")
            if author in sentinels:
                return

            novel = input("Enter title of book to modify. >>> ")
            if novel in sentinels:
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

    elif (result == "Start") or (result == "Start Date") or (result == "S"):
        while True:
            author = input("Enter name(s) of author/authors book is associated with. >>> ")
            if author in sentinels:
                return

            novel = input("Enter title of book date is associated with. >>> ")
            if novel in sentinels:
                return

            start_date = input("Enter start date to modify. >>> ")
            if start_date in sentinels:
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

    elif (result == "End") or (result == "End Date") or (result == "E"):
        while True:
            author = input("Enter name(s) of author/authors book is associated with. >>> ")
            if author in sentinels:
                return

            novel = input("Enter title of book date is associated with. >>> ")
            if novel in sentinels:
                return

            end_date = input("Enter end date to modify. >>> ")
            if end_date in sentinels:
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

    else:
        print("Invalid, try again.")


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


def import_json():
    try:
        with open(json_path, "r") as file:
            data_dict = json.load(file)
    except FileNotFoundError:
        print("No data available currently to import, this should change once book log begins.\n")
        data_dict = {}
        return data_dict
    else:
        return data_dict


def start_entry(data):
    name = input("Enter name(s) of author/authors. >>> ").strip()
    book = input("Enter title of book. >>> ").strip()
    check_data_structure(data, name, book)
    date1 = timestamp()
    date2 = "N/A"
    data[name][book]["Start Date"] = date1
    data[name][book]["End Date"] = date2

    add_file_header(is_file_empty(txt_path), txt_file_line, txt_path)
    with open(txt_path, "a") as file:
        file.write(txt_file_line.format(col1=name, col2=book, col3=date1, col4=date2))

    try:
        add_file_header(is_file_empty(csv_path), csv_file_line, csv_path)
        with open(csv_path, "a") as file:
            file.write(csv_file_line.format(col1=name, col2=book, col3=date1, col4=date2))
    except PermissionError:
        print("Unable to write new data to csv file, please close the program the file is opened in and try again.")
        print("(You can use the 'Push' command to write all data back to file once the program is closed)")
    finally:
        with open(json_path, "w") as file:
            json.dump(data, file, indent=4)


def end_entry(data):
    name = input("Enter name(s) of author/authors. >>> ").strip()
    book = input("Enter title of book. >>> ").strip()
    check_data_structure(data, name, book)
    date2 = timestamp()
    result = start_date_check(data, name, book)
    modify_start_date(data, result, name, book)
    data[name][book]["End Date"] = date2


def display_txt_file():
    try:
        with open(txt_path, "r") as file:
            for line in file:
                print(line.rstrip())
    except FileNotFoundError:
        print("No book-log.txt file found, please add entries before using this command.\n")


def display_modifier_options():
    prompt = ("Which field would you like to modify?\n\n"
              "Author/Authors : A\n"
              "Book Title : B\n"
              "Start Date : S\n"
              "End Date : E\n"
              "Quit : Q\n\n"
              ">>> ")
    result = input(prompt).strip().lower()
    return result


def dump_to_files(data):
    with open(txt_path, "w") as file:
        file.write(txt_file_line.format(
            col1=cell1, col2=cell2, col3=cell3, col4=cell4))
        for name, books in data.items():
            for book, dates in books.items():
                date1 = dates.get("Start Date", "N/A")
                date2 = dates.get("End Date", "N/A")
                file.write(f"{name:40} | {book:40} | {date1:20} | {date2:20}\n")
    try:
        with open(csv_path, "w") as file:
            file.write(csv_file_line.format(
                col1=cell1, col2=cell2, col3=cell3, col4=cell4))
            for name, books in data.items():
                for book, dates in books.items():
                    date1 = dates.get("Start Date", "N/A")
                    date2 = dates.get("End Date", "N/A")
                    file.write(f'"{name}","{book}",{date1},{date2}\n')
    except PermissionError:
        print("Unable to write new data to csv file, close other program and run this command again.")
        print("(You can use the 'Push' command to write all data back to file once the program is closed)")
    finally:
        with open(json_path, "w") as file:
            json.dump(data, file, indent=4)


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
            dump_to_files(program_data)
        elif user_input == "Push":
            dump_to_files(program_data)
        else:
            print("Unknown command, please try again.")

        print()
        user_input = input(program_options[19:]).strip().lower().title()

    print(program_data)


# Get the user's home directory
home_directory = os.path.expanduser('~')

# Create a "Documents" directory path within the home directory
documents_directory = os.path.join(home_directory, 'Documents')

cell1 = "Author/Authors"
cell2 = "Book Title"
cell3 = "Start Date"
cell4 = "End Date"

txt_filename = "book-log.txt"
txt_path = os.path.join(documents_directory, txt_filename)
txt_file_line = '{col1:40} | {col2:40} | {col3:20} | {col4:20}\n'

csv_filename = "book-log.csv"
csv_path = os.path.join(documents_directory, csv_filename)
csv_file_line = '"{col1}","{col2}","{col3}","{col4}"\n'

json_filename = "book-logger.json"
json_path = os.path.join(os.path.dirname(__file__), json_filename)

if __name__ == "__main__":
    main()
