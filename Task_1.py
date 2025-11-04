from collections import UserDict
import re

# Базовий клас для полів
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для імені (обов'язкове поле)
class Name(Field):
    pass

# Клас для телефону з валідацією
class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

# Клас для одного запису контакту
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_value):
        phone = Phone(phone_value)
        self.phones.append(phone)

    def remove_phone(self, phone_value):
        phone_to_remove = None
        for phone in self.phones:
            if phone.value == phone_value:
                phone_to_remove = phone
                break
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
            return True
        return False

    def edit_phone(self, old_phone_value, new_phone_value):
        for idx, phone in enumerate(self.phones):
            if phone.value == old_phone_value:
                self.phones[idx] = Phone(new_phone_value)
                return True
        return False

    def find_phone(self, phone_value):
        for phone in self.phones:
            if phone.value == phone_value:
                return phone.value
        return None

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

# Клас для адресної книги
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

# Приклад використання
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

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
    print("\nAfter deleting Jane:")
    for name, record in book.data.items():
        print(record)
