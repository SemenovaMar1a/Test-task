import json
from typing import List, Dict, Tuple, Optional

FILE_PATH = 'library.json'

# Структура данных по умолчанию для нового JSON-файла.
DEFAULT_STRUCTURE = {
    "catalog": {}
}

def save_json(data: Dict) -> None:
    """
    Сохраняет данные в JSON-файл.

    Аргументы:
    data (Dict): Словарь, который нужно сохранить в файл.

    Возвращаемое значение:
    None: Функция ничего не возвращает.
    """
    with open(FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_json_or_create() -> Dict:
    """
    Загружает JSON-файл, если он существует, или создает новый файл
    с структурой по умолчанию.

    Возвращаемое значение:
    Dict: Загруженные или созданные данные в виде словаря.
    """
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {FILE_PATH} не найден. Создаём новый.")
        save_json(DEFAULT_STRUCTURE)
        return DEFAULT_STRUCTURE
    except json.JSONDecodeError:
        print(f"Файл {FILE_PATH} повреждён. Перезаписываем.")
        save_json(DEFAULT_STRUCTURE)
        return DEFAULT_STRUCTURE

def add_book(book_title: str, author_name: str, publication_year: int) -> None:
    """
    Добавляет новую книгу в каталог.

    Аргументы:
    book_title (str): Название книги.
    author_name (str): Имя автора.
    publication_year (int): Год издания книги.

    Возвращаемое значение:
    None: Функция ничего не возвращает.
    """
    data = load_json_or_create()
    book_dict = {"title": book_title, 'author': author_name, 'year': publication_year, 'status': 'в наличии'}

    # создание ID
    if not data["catalog"]:
        new_id = 1
    else:
        new_id = max(int(key) for key in data["catalog"].keys()) + 1

    # добавление записи в каталог
    data["catalog"][str(new_id)] = book_dict
    save_json(data)

def remove_book(id_to_delete: str) -> bool:
    """
    Удаляет книгу из каталога по её ID.

    Аргументы:
    id_to_delete (str): ID книги, которую нужно удалить.

    Возвращаемое значение:
    bool: Возвращает True, если книга была удалена, и False, если книга с таким ID не найдена.
    """
    data = load_json_or_create()

    if id_to_delete in data['catalog']:
        del data['catalog'][id_to_delete]
        save_json(data)
        return True
    else:
        return False

def search_book(search_key: str) -> List[Tuple[str, Dict]]:
    """
    Ищет книги по параметрам (название, автор или год издания).

    Аргументы:
    search_key (str): Ключ для поиска (может быть названием, автором или годом).

    Возвращаемое значение:
    List[Tuple[str, Dict]]: Список найденных книг, где каждый элемент
    является кортежем с ID книги и словарем с данными книги.
    """
    data = load_json_or_create()

    found_books = []
    for id, book_data in data['catalog'].items():
        if search_key.isdigit():
            if int(book_data.get('year', 0)) == int(search_key):
                found_books.append((id, book_data))
        else:
            if book_data.get('author', '').lower() == search_key.lower():
                found_books.append((id, book_data))
            elif book_data.get('title', '').lower() == search_key.lower():
                found_books.append((id, book_data))

    return found_books

def change_status(book_id: str, new_status: str) -> bool:
    """
    Меняет статус книги по её ID (например, "в наличии" или "выдана").

    Аргументы:
    book_id (str): ID книги, для которой нужно изменить статус.
    new_status (str): Новый статус книги (например, "в наличии" или "выдана").

    Возвращаемое значение:
    bool: Возвращает True, если статус был успешно изменён, и False, если книга с таким ID не найдена.
    """
    data = load_json_or_create()
    for id, book_data in data['catalog'].items():
        if id == book_id:
            book_data['status'] = new_status
            break
    else:
        return False

    save_json(data)
    return True

# Главный цикл программы
while True:
    # Получение данных из файла
    data = load_json_or_create()

    # Меню выбора действий
    print("\n1. Добавить книгу")
    print("2. Удалить книгу")
    print("3. Поиск книги")
    print("4. Показать каталог книг")
    print("5. Сменить статус")
    print("6. Выйти")

    choice = input("Выберите действие: ")

    # добавление новой книги в каталог
    if choice == '1':
        title = input('Введите название книги ')
        author = input('Введите автора книги ')
        year = int(input('Введите год издания '))

        add_book(title, author, year)

    # удаление книги по ID
    elif choice == '2':
        id_removal = input('Введите id книги, которую нужно удалить ')
        result_remove = remove_book(id_removal)

        if result_remove:
            print('Запись успешно удалена')
        else:
            print('Записи с таким ID нет')

    # поиск книги по параметрам
    elif choice == '3':
        search = input('Введите автора или название книги или год для поиска ')

        result_search = search_book(search)

        if result_search:
            for id, book in result_search:
                print(f"\nID: {id}\nНазвание: {book['title']}\nАвтор: {book['author']}\nГод: {book['year']}\nСтатус: {book['status']}\n")
        else:
            print('Таких книг нет')

    # вывод всех книг из каталога
    elif choice == '4':
        if data:
            print("Все книги в каталоге:")
            for id, item in data['catalog'].items():
                print(f'\nID: {id}\nНазвание: {item["title"]}\nАвтор: {item["author"]}\nГод: {item["year"]}\nСтатус: {item["status"]}\n')
        else:
            print("Файл пуст или недоступен.")

    # нахождение книги по ID и смена статуса
    elif choice == '5':
        book_id = input('Введите ID книги ')
        new_status = input('Введите новый статус (он может быть либо "В наличии" либо "Выдана") ')

        result_change = change_status(book_id, new_status)

        if result_change:
            print('Статус изменен успешно')
        else:
            print('Такого ID нет')

    # выход из программы
    elif choice == '6':
        print("Выход.")
        break
    else:
        print("Неверный выбор. Попробуйте ещё раз.")
