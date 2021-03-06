# -*- coding: utf-8 -*-

import sys
from argparse import ArgumentParser
from code_stat_collector.collector import StatCollector
from exceptions import FetchRepoError, OutputError

# todo Подумать над типами параметров. Возможно, запилить для них Enumeration
# todo Спросить у Ильи насчет использования Enumeration вместо строк для обозначения частей речи, вывода и подобного


def main():
    try:
        return_code = 0
        parser = ArgumentParser(prog='csc', description='Подсчет статистики в исходном коде приложений.')
        parser.add_argument('url', type=str, help='Ссылка на репозиторий с исходным кодом'),
        parser.add_argument('-l', '--lang', nargs='?', default='py', type=str,
                            help='Язык программирования'),
        parser.add_argument('-p', '--pos', nargs='?', default='verb', type=str, choices=['noun', 'verb'],
                            help='Анализируемые части речи. noun - существительные; verb - глаголы')
        parser.add_argument('-с', '--code_element', nargs='?', default='func', type=str, choices=['loc_var', 'func'],
                            help='Анализируемые части кода. var - локальные переменные внутри функций;'
                                 'func - названия функций')
        parser.add_argument('-o', '--output', nargs='?', default='stdout', type=str, choices=['stdout', 'file'],
                            help='Место вывода отчета. stdout - консоль; file - файл')
        parser.add_argument('-f', '--format', nargs='?', default='json', type=str, choices=['json', 'csv'],
                            help='Формат вывода отчета. json - json-файл; csv - csv-файл')
        parser.add_argument('-t', '--top', nargs='?', default='10', type=int,
                            help='Количество частей речи, выводимых в статистике (топ)')
        parser.add_argument('-n', '--file', nargs='?', type=str,
                            help='Путь к файлу, если требуется выводить статистику в файл')
        args = parser.parse_args(sys.argv[1:])

        settings = dict(url=args.url,
                        lang=args.lang,
                        code_element=args.code_element,
                        part_of_speech=args.pos,
                        output=args.output,
                        format=args.format,
                        top=args.top,
                        file=args.file)

        collector = StatCollector(settings)
        stat = collector.collect_stat()
        collector.output_stat(stat)

    except (FetchRepoError, OutputError) as e:
        print(e)
        return_code = 2

    except Exception as e:
        print('Неопределенная ошибка в приложении: {exception}'.format(exception=e))
        return_code = 1

    return return_code
