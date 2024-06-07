from functools import wraps
from birthdaysoon import get_upcoming_birthdays
from addressbooklb import Record
import pickle
from addressbooklb import AddressBook


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Декоратор для виправлення помилок.
def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:

            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found. Use 'add' command instead"
        except IndexError:
            return "Enter the argument for the command"

    return inner


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if not record:
        raise ValueError("Contact not found")
    phone = record.find_phone(old_phone)
    if phone:
        record.remove_phone(old_phone)
        record.add_phone(new_phone)
        return "Phone number changed."
    else:
        return "Phone number not found for this contact."


@input_error
def phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record:
        result = [person_phone.value for person_phone in record.phones]
        return f'Person phone : \n{"\n".join(result)}'
    else:
        return "Contact not found."


def show_all(book):
    items = list()
    for name, record in book.data.items():
        person = f'Name {name} , '
        person = person + f'phones: {'; '.join(phone.value for phone in record.phones)}'
        if record.birthday != None:
            person = person + ', birthday: ' + record.birthday.value.strftime("%d.%m.%Y")
        items.append(person)
    return f'Your contacts : \n{'\n'.join(items)}'

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        return f"Contact '{name}' not found."


@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    birthday = record.birthday
    if birthday:
        return f'Birthday of {name} : {birthday.value.strftime("%d.%m.%Y")}'
    else:
        return "I don't find a birthday"


def birthdays(book):
    list_birthdays = []
    soon_birthdays = []
    for name in book:
        list_birthdays.append(
            {"name": name, "birthday": book.find(name).birthday.value}
        )

    soon_birthdays = get_upcoming_birthdays(list_birthdays)
    if soon_birthdays:
        print("List of upcoming birthdays: ")
        return f"{'\n'.join([f'{my_dict['name']} : {my_dict['congratulation_date']}' for my_dict in soon_birthdays])}"
    else:
        return "Have no upcoming birthdays"


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
