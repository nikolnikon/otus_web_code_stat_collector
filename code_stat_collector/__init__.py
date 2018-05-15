# -*- coding: utf-8 -*-

import sys
from argparse import ArgumentParser
from code_stat_collector.collector import StatCollector

# todo Подумать над типами параметров. Возможно, запилить для них Enumeration


def main():
    try:
        return_code = 0
        parser = ArgumentParser('Подсчет самых популярных существительных в заголовках статей с сайта habr.com')
        parser.add_argument('-p', '--pos', nargs='?', default='verb', type=str, choices=['noun', 'verb'],
                            help='Анализируемые части речи. noun - существительные; verb - глаголы')
        parser.add_argument('-с', '--code_element', nargs='?', default='method', type=str, choices=['loc_var', 'func'],
                            help='Анализируемые части кода. var - локальных переменных внутри функций;'
                                 'func - названия функций')
        parser.add_argument('-o', '--output', nargs='?', default='stdout', type=str, choices=['stdout', 'file'],
                            help='Место вывода отчета. stdout - консоль; file - файл')
        parser.add_argument('-f', '--format', nargs='?', default='json', type=str, choices=['json', 'csv'],
                            help='Формат вывода отчета. json - json-файл; csv - csv-файл')
        args = parser.parse_args(sys.argv[1:])

        settings = dict(lang=args.lang,
                        code_element=args.code_element,
                        part_of_speech=args.pos,
                        output=args.output,
                        format=args.format)

        collector = StatCollector(settings)
        stat = collector.collect_stat()
        collector.output_stat(stat)

    except Exception as e:
        print('Неопределенная ошибка в приложении: {exception}'.format(exception=e))
        return_code = 1

    return return_code
