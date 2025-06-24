import requests


ERROR_TEXT = f'Ошибка выполнения запроса.'
LIMIT_TEXT = f'Превышено число запросов. Попробуйте позже.'


def main(username: str):
    """
    При успешном запросе выводит аналитику профиля пользователя на экран
    :param username: str
    :return:
    """
    print(f'Аналитика профиля GitHub: {username}')
    for key, value in repository_analytics(username).items():
        print(f'{key}: {value}')
    print('Топ языков программирования: ')
    for kort in languages_analytics(username):
        print(f'- {kort[0]}: {kort[1]} репозит.')


def do_request():
    """
    Делает запрос, обрабатывает ошибки, запускает основную функцию main в случае успешного запроса
    :return:
    """
    user = input('Введите имя пользователя: ')
    try_url = f'https://api.github.com/users/{user}'
    resp = requests.get(try_url)
    if resp.status_code == 200:
        main(user)
    elif resp.status_code == 403:
        print(LIMIT_TEXT)
    else:
        print(ERROR_TEXT)


def repository_analytics(username: str) -> dict:
    """
    Формирует аналитику репозиториев профиля
    :param username: str
    :return: dict
    """
    stars_dict = stars_counter(username)
    info = {
        'Количество публичных репозиториев': len(get_repos(username)),
        'Общее количество звёзд': sum(list(stars_dict.values())),
        'Самый популярный репозиторий': f'{popular_repo(stars_dict)[0]} (⭐ {popular_repo(stars_dict)[1]} звёзд)'
            }
    return info


def languages_analytics(username: str) -> list[tuple]:
    """
    Формирует аналитику используемых языков
    :param username: str
    :return: list
    """
    return popular_language(get_language(get_repos(username)))


def get_repos(username: str) -> list[dict]:
    """
    Возвращает список репозиториев пользователя
    :param username: str
    :return: list
    """
    url = f'https://api.github.com/users/{username}/repos'
    return requests.get(url).json()


def stars_counter(username: str) -> dict:
    """
    Возвращает словарь: ключ - имя репозитория, значение - кол-во звезд
    :param username: str
    :return: dict
    """
    repos = {}
    for repo in get_repos(username):
        repos[repo['name']] = repo['stargazers_count']
    return repos


def popular_repo(stars_dict: dict) -> tuple:
    """
    Возвращает самый "звёздный" кортеж: имя репозитория и кол-во звезд
    :param stars_dict: dict
    :return: tuple
    """
    return max(stars_dict.items(), key=lambda item: item[1])


def get_language(repos: list[dict]) -> dict:
    """
    Возвращает словарь: ключ - название языка, значение - кол-во звезд
    :param repos: list
    :return: dict
    """
    languages_dict = {}
    for repo in repos:
        if repo['language'] is not None:
            languages_dict[repo['name']] = repo['language']
    return languages_dict


def popular_language(language_dict: dict) -> list[tuple]:
    """
    Возвращает список, содержащий кортежи с парой значений "язык программирования" и "кол-во репозиториев"
    :param language_dict:
    :return:
    """
    dct = {value: list(language_dict.values()).count(value) for value in set(language_dict.values())}
    top_lang = sorted(dct.items(), key=lambda item: item[1], reverse=True)
    return top_lang


do_request()