# otus_web_code_stat_collector

Приложение для подсчета статистики в исходном коде приложений. Умеет считать самые популярные существительные или 
глаголы в названиях функций или локальных переменных.

## Установка

С использованием git и easy_install:
```bash
$ git clone https://github.com/nikolnikon/otus_web_code_stat_collector.git
$ cd otus_web_code_stat_collector
$ sudo python setup.py install
$ python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('averaged_perceptron_tagger')
```

С использованием git и установкой зависимостей из requirements.txt (для разработки):
```bash
$ git clone https://github.com/nikolnikon/otus_web_code_stat_collector.git
$ cd otus_web_code_stat_collector
$ pip install -r requirements.txt
$ python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('averaged_perceptron_tagger')
```

## Пример использования

```bash
$ /usr/bin/csc https://github.com/nikolnikon/otus_web_code_stat_collector.git
{"project": "https://github.com/nikolnikon/otus_web_code_stat_collector.git", "part of speech": "verb", "statistics": {"parse": 2, "get": 5, "count": 1, "collect": 1, "serialize": 1, "build": 1, "create": 1}, "element_of_code": "func"}

$ /usr/bin/csc https://github.com/nikolnikon/otus_web_code_stat_collector.git --pos=verb --code_element=func --output=stdout --format=csv --top=15
get,5
parse,2
serialize,1
build,1
count,1
create,1
collect,1
```

## Документация
Параметры запуска приложения доступны в справке:

```bash
$ /usr/bin/csc --help
usage: csc [-h] [-l [LANG]] [-p [{noun,verb}]] [-с [{loc_var,func}]]
           [-o [{stdout,file}]] [-f [{json,csv}]] [-t [TOP]] [-n [FILE]]
           url

Подсчет статистики в исходном коде приложений.

positional arguments:
  url                   Ссылка на репозиторий с исходным кодом

optional arguments:
  -h, --help            show this help message and exit
  -l [LANG], --lang [LANG]
                        Язык программирования
  -p [{noun,verb}], --pos [{noun,verb}]
                        Анализируемые части речи. noun - существительные; verb
                        - глаголы
  -с [{loc_var,func}], --code_element [{loc_var,func}]
                        Анализируемые части кода. var - локальные переменные
                        внутри функций;func - названия функций
  -o [{stdout,file}], --output [{stdout,file}]
                        Место вывода отчета. stdout - консоль; file - файл
  -f [{json,csv}], --format [{json,csv}]
                        Формат вывода отчета. json - json-файл; csv - csv-файл
  -t [TOP], --top [TOP]
                        Количество частей речи, выводимых в статистике (топ)
  -n [FILE], --file [FILE]
                        Путь к файлу, если требуется выводить статистику в
                        файл
```

## Версионирование
Используется подход [semantic versioning](https://github.com/dbrock/semver-howto/blob/master/README.md).

## Лицензия
Проект распространяентся под лицензией MIT. Подробная информация в файле
[LICENSE](https://github.com/nikolnikon/otus-web-refactoring/blob/master/LICENSE)
