class FetchRepoError(Exception):
    def __init__(self, url, message=None):
        super(FetchRepoError, self).__init__('Ошибка при клонировании репозитория {url}. {message}'.format(
            url=url,
            message=message))


class OutputError(Exception):
    def __init__(self, message=None):
        super(OutputError, self).__init__('Ошибк при записи статистики в файл. {message}'.format(message=message))
