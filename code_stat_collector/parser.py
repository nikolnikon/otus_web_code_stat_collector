import ast
import tempfile
import os
import subprocess
from abc import ABCMeta, abstractmethod
from code_stat_collector.utils import flat, split_words_by_underscore, get_files_names
from exceptions import FetchRepoError


class AbstractParser(metaclass=ABCMeta):
    def __init__(self, url):
        self._url = url

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @abstractmethod
    def get_words(self, code_element):
        raise NotImplementedError('Не определен метод get_words')

    @abstractmethod
    def _parse(self):
        raise NotImplementedError('Не определен метод _parse')

    def _fetch_source_code(self):
        temp_path = tempfile.mkdtemp()
        proc = subprocess.Popen(['git', 'clone', self._url, temp_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            outs, errs = proc.communicate()
        except (OSError, ValueError, subprocess.SubprocessError) as e:
            raise FetchRepoError(self._url, str(e)) from e

        res = proc.returncode
        if res:
            if res != 0:
                raise FetchRepoError(self._url, '{message}, код возврата: {code}'.format(message=errs, code=res))
        return temp_path


class PythonParser(AbstractParser):
    def __init__(self, url):
        super(PythonParser, self).__init__(url)
        self._trees = []

    def get_words(self, code_element):
        self._parse()
        return self._get_words_from_elements_names(code_element)

    def _parse(self):
        if self._trees:
            return

        path = self._fetch_source_code()
        self._build_trees(path)

    def _build_trees(self, path):
        """
        Находит файлы с расширением .py и строит из их содержимого деревья с помощью ast
        :param path:                Путь к дирктории, внутри которой искать файлы
        """
        py_filenames = []
        for dirname, dirs, files in os.walk(path, topdown=True):
            py_filenames += get_files_names(dirname, files, 'py')

        for filename in py_filenames:
            with open(filename, 'r', encoding='utf-8') as attempt_handler:
                main_file_content = attempt_handler.read()
                try:
                    tree = ast.parse(main_file_content)
                    self._trees.append(tree)
                except SyntaxError as e:
                    pass

    def _get_words_from_elements_names(self, code_element):
        names = []
        if code_element == 'func':
            names = flat([self._get_all_functions_names(t) for t in self._trees])
        elif code_element == 'loc_var':
            names = flat([self._get_all_local_variables_names(t) for t in self._trees])
        words = flat([split_words_by_underscore(name) for name in names])
        return words

    def _get_all_functions_names(self, tree):
        """
        Возвращает список имен всех функций в дереве (файле), за исключением системных
        :return:        Список имен всех функций в дереве, за исключением системных
        """
        all_funcs = [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return [f for f in all_funcs if not (f.startswith('__') and f.endswith('__'))]

    def _get_all_local_variables_names(self, tree):
        func_bodies = [node.body for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return flat([[a.targets[0].id for a in fb if isinstance(a, ast.Assign) and isinstance(a.targets[0], ast.Name)] for fb in func_bodies])



