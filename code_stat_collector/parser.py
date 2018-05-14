import os
import ast
import itertools


class AbstractParser:
    def __init__(self, url):
        self._url = url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    def get_words(self, code_element):
        pass

    def _fetch_source_code(self):
        path = str()
        return path

    def _parse(self):
        pass


class PythonParser(AbstractParser):
    def __init__(self, url):
        super(PythonParser, self).__init__(url)
        self._trees = []

    def get_words(self, code_element):
        self._parse()
        # todo Посмотреть, как делается связывание методов класса
        # funcs = dict(
        #     func=
        #
        # )
        words = []

    def _parse(self):
        if self._trees:
            return

        path = self._fetch_source_code()
        self._get_trees(path)

    def _get_trees(self, path):
        """
        Находит файлы с расширением .py и строит из их содержимого деревья с помощью ast
        :param path:                Путь к дирктории, внутри которой искать файлы
        """
        py_filenames = []
        for dirname, dirs, files in os.walk(path, topdown=True):
            py_filenames += self._get_py_files_names(dirname, files)

        for filename in py_filenames:
            with open(filename, 'r', encoding='utf-8') as attempt_handler:
                main_file_content = attempt_handler.read()
                try:
                    tree = ast.parse(main_file_content)
                except SyntaxError as e:
                    tree = None

            self._trees.append(tree)

    def _get_py_files_names(self, dirname, files):
        py_filenames = []
        for file in files:
            if file.endswith('.py'):
                py_filenames.append(os.path.join(dirname, file))

    def _get_words_from_funtions_names(self):
        funcs = self._flat([self._get_all_functions_names(t) for t in self._trees])
        words = self._flat([self._get_words_from_function_name(function_name) for function_name in funcs])
        return words

    def _get_words_from_variables_names(self):
        pass

    # todo Сделать один метод для получения всех слов из функции или из переменной
    def _get_all_functions_names(self, tree):
        """
        Возвращает список имен всех функций в дереве (файле), за исключением системных
        :return:        Список имен всех функций в дереве, за исключением системных
        """
        all_funcs = [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return [f for f in all_funcs if not (f.startswith('__') and f.endswith('__'))]

    def _get_words_from_function_name(self, function_name):
        """
        Возвращает список слов, входящих в название функции
        :param function_name:   Название функции
        :return:                Список слов, входящих в название функции
        """
        return [word for word in function_name.split('_')]

    def _flat(self, _list):
        """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
        return [i for i in itertools.chain.from_iterable(_list)]
