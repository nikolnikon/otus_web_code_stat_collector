from code_stat_collector.analyzer import Analyzer
from code_stat_collector.parser import PythonParser
from code_stat_collector.serializer import JSONSerializer, CSVSerializer
from exceptions import OutputError


class StatCollector:
    def __init__(self, settings):
        self._settings = settings
        self._parser = self._create_parser()
        self._analyzer = Analyzer()
        self._serializer = self._create_serializer()

    def collect_stat(self):
        words = self._parser.get_words(self._settings['code_element'])
        stat = self._analyzer.get_words_count(words, self._settings['part_of_speech'], self._settings['top'])
        return stat

    def output_stat(self, stat):
        output = self._serializer.serialize(stat, self._settings)
        if self._settings['output'] == 'stdout':
            print(output)
        elif self._settings['output'] == 'file':
            if not self._settings['file']:
                raise OutputError('Путь к выходному файлу не задан')
            with open(self._settings['file'], 'w+') as f:
                f.write(output)

    def _create_parser(self):
        if self._settings['lang'] == 'py':
            return PythonParser(self._settings['url'])

    def _create_serializer(self):
        if self._settings['format'] == 'json':
            return JSONSerializer()
        elif self._settings['format'] == 'csv':
            return CSVSerializer()
