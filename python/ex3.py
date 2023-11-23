from typing import Callable


def caesar_encrypter(text: str, shift: int, alphabet: str) -> str:
    result = ''

    for char in text:
        if char.upper() in alphabet:
            if char.isupper():
                result += alphabet[(alphabet.index(char) + shift) % len(alphabet)]
            else:
                result += alphabet[(alphabet.index(char.upper()) + shift) % len(alphabet)].lower()
        else:
            result += char

    return result


def get_encrypter(language: str, shift: int) -> Callable[[str], str]:
    if language == 'e':
        return lambda text: caesar_encrypter(text, shift, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    elif language == 'r':
        return lambda text: caesar_encrypter(text, shift, 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
    else:
        raise ValueError("Неподдерживаемый язык")


def encrypt_file(input_file: str, output_file: str, enctypter: Callable[[str], str]) -> None:
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        encrypted_text = enctypter(text)
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(encrypted_text)

        print(f"Шифрование завершено. Результат записан в файл {output_file}")
    except FileNotFoundError:
        print("Ошибка: Указанный файл не найден")
    except Exception as e:
        print(f"Ошибка: {e}")


input_file_path = input("Введите путь до изначального файла с текстом: ")
output_file_path = input("Введите путь для нового файла с зашифрованным текстом: ")

try:
    shift = int(input("Введите сдвиг для шифрования: "))
    language = input("Выберите язык текста ('e' или 'r'): ")
    encrypter = get_encrypter(language, shift)

    encrypt_file(input_file_path, output_file_path, encrypter)
    encrypt_file(output_file_path, input_file_path + '_', get_encrypter(language, -shift))

except Exception as e:
    print(f"Ошибка: {e}")
