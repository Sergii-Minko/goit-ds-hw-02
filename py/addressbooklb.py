from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
            if len(value.split(".")) != 3:
                raise ValueError("Invalid date format. Use DD.MM.YYYY")
            day, month, year = map(int, value.split("."))

            if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year):
                raise ValueError("Invalid date format. Use DD.MM.YYYY")

            if datetime(year, month, day) > datetime.now():
                raise ValueError("Invalid date. Birthday cannot be in the future.")
            self.value = datetime(year, month, day)
            print(self.value)

        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Name(Field):
    def __init__(self, name):
        self.value = name


class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise ValueError("Номер телефону повинен містити рівно 10 цифр")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)
        return self.phones

    def edit_phone(self, edit_number, new_number):
        phone = self.find_phone(edit_number)
        if phone:
            self.phones[self.phones.index(phone)] = Phone(new_number)
            return self.phones
        else:
            raise ValueError(f"Телефонний номер {edit_number} не знайдено.")

    def find_phone(self, search_number):
        for phone in self.phones:
            if phone.value == search_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, contact):
        self.data[contact.name.value] = contact

    def find(self, key):
        result = self.data.get(key)
        return result

    def delete(self, key):
        self.data.pop(key, None)
