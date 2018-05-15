import itertools
import os


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return [i for i in itertools.chain.from_iterable(_list)]


def split_words_by_underscore(function_name):
    """
    get_my_bag -> ['get', 'my', 'bag']
    """
    return [word for word in function_name.split('_')]


def get_files_names(dirname, files, extension):
    files_names = []
    for file in files:
        if file.endswith('.{extension}'.format(extension=extension)):
            files_names.append(os.path.join(dirname, file))

    return files_names
