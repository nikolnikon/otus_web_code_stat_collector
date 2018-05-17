from abc import ABCMeta, abstractmethod
import json
import sys
import csv
import io


class AbstractSerializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, stat, settings):
        raise NotImplementedError('Не определен метод serialize')


class JSONSerializer(AbstractSerializer):
    def serialize(self, stat, settings):
        output_dict = {
            'project': settings['url'],
            'element_of_code': settings['code_element'],
            'part of speech': settings['part_of_speech'],
            'statistics': {s[0]: s[1] for s in stat},
        }

        return json.dumps(output_dict)


class CSVSerializer(AbstractSerializer):
    def serialize(self, stat, settings):
        rows = [[s[0], s[1]] for s in stat]
        str_io = io.StringIO()
        csv_writer = csv.writer(str_io)
        csv_writer.writerows(rows)
        output = str_io.getvalue()
        str_io.close()
        return output
