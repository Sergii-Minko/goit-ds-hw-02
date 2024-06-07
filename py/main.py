from addressbooklb import AddressBook
from bot import *


def main():
    book = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "help":
            print(
                "Available commands:\nadd <name> <phone>\nchange <name> <phone>\nphone <name>\nall\nadd-birthday <name> <birthday>\nshow-birthday <name>\nbirthdays\nexit\n"
            )
        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
