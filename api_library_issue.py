import requests


# Общие функции
def exception_handling(response: requests.models.Response):
    """
    Обрабатывает потенциальные ошибки запроса
    :param response: requests.models.Response
    :return:
    """
    if response.status_code == 200:
        return
    elif response.status_code == 403:
        raise requests.exceptions.HTTPError('Превышен лимит запросов. Попробуйте позже')
    raise requests.exceptions.HTTPError('Ошибка запроса')


# Работа с поиском по автору
def author_main():
    """
    При успешном запросе выводит информацию о книгах автора в библиотеке
    :return:
    """
    author = author_input()
    books = get_authors_books(author)
    print(f'Количество книг автора в библиотеке: {get_length(get_titles(books))}')
    print('Список книг:')
    for book in get_titles(books):
        print(f'- "{book}"')

def author_input() -> str:
    """
    Принимает имя автора, возвращает версию для подстановки в url
    :return: str
    """
    author = input('Введите имя автора на английском: ').lower().strip()
    return author.replace(" ", "+")

def get_authors_books(author: str) -> list[dict]:
    """
    Возвращает список словарей с информацией о книгах автора
    :param author: str
    :return: dict
    """
    url = f'https://openlibrary.org/search.json?author={author}'
    response = requests.get(url)
    exception_handling(response)
    return response.json()['docs']

def get_titles(books_list: list[dict]) -> set:
    """
    Возвращает уникальные заголовки книг автора
    :param books_list: list[dict]
    :return: set
    """
    book_set = set()
    for book in books_list:
        book_set.add(book['title'].title())
    return book_set

def get_length(items_set: set) -> int:
    """
    Возвращает кол-во уникальных заголовков
    :param items_set: set
    :return: int
    """
    return len(items_set)

#author_main()


# Работа с поиском по книге
def book_main():
    """
    При успешном запросе выводит информацию об искомой книге
    :return:
    """
    book = book_input()
    book_info = get_info_book(book)
    print('Имя автора:', *get_author(book_info))
    print(f'Дата публикации: {get_publish_year(book_info)}')
    print(f'Наличие русскоязычной версии на сайте: {is_russian_lang(book_info)}')

def book_input() -> str:
    """
    Принимает название книги, возвращает версию для подстановки в url
    :return: str
    """
    book = input('Введите название книги на английском: ').lower().strip()
    return book.replace(" ", "+")

def get_info_book(book: str) -> dict:
    """
    Возвращает информацию о первом найденном в библиотеке совпадении в виде словаря
    :param book: str
    :return: dict
    """
    url = f'https://openlibrary.org/search.json?title={book}'
    response = requests.get(url)
    exception_handling(response)
    return response.json()['docs'][0]

def get_author(book_dict: dict) -> list:
    """
    Возвращает список, содержащий автора/авторов книги
    :param book_dict: dict
    :return: list
    """
    return book_dict['author_name']

def get_publish_year(book_dict: dict) -> int:
    """
    Возвращает год издания найденной в библиотеке книги
    :param book_dict: dict
    :return: int
    """
    return book_dict['first_publish_year']

def is_russian_lang(book_dict: dict) -> bool:
    """
    Проверяет наличие русскоязычной версии, возвращает булевое значение
    :param book_dict: dict
    :return: bool
    """
    if book_dict['language']:
        if 'rus' in book_dict['language']:
            return True
    return False

#book_main()