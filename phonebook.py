import re
from collections import UserDict
from typing import List
from constants import PHONE_REGEXP


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, contact_name):
        if not contact_name:
            raise ValueError("Name cannot be empty")
        super().__init__(contact_name)


class Phone(Field):
    def __init__(self, phone):
        if not re.match(PHONE_REGEXP, phone):
            raise ValueError("Phone number must consist of 10 digits")
        super().__init__(phone)


class Record:
    def __init__(self, contact_name: str) -> None:
        self.name = Name(contact_name)
        self.phones: List[Phone] = []

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        for phone_item in self.phones:
            if phone_item.value == phone:
                return self.phones.remove(phone_item)
        raise ValueError(f"Phone number {phone} not found")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        if not re.match(PHONE_REGEXP, new_phone):
            raise ValueError("Phone number must consist of 10 digits")
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError(f"Phone number {old_phone} not found")

    def find_phone(self, phone: str) -> Phone:
        for phone_item in self.phones:
            if phone_item.value == phone:
                return phone_item
        raise ValueError(f"Phone number {phone} not found")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {
            '; '.join(p.value for p in self.phones)
        }"


class AddressBook(UserDict):
    def add_record(self, new_record: Record) -> None:
        if new_record.name.value in self.data:
            raise ValueError(f"Contact {new_record.name.value} already exists")
        self.data[new_record.name.value] = new_record

    def find(self, contact_name: str) -> Record:
        if contact_name not in self.data:
            raise ValueError(f"Contact {contact_name} not found")
        return self.data[contact_name]

    def delete(self, contact_name: str) -> None:
        if contact_name not in self.data:
            raise ValueError(f"Contact {contact_name} not found")
        del self.data[contact_name]


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
