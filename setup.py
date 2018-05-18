# -*- coding: utf-8 -*-

from os.path import join, dirname
from setuptools import setup, find_packages

setup(
    name='code_stat_collector',
    version='0.0.1',
    description='Приложение для подсчета статистики в исходном коде приложений',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='nikolnikon',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    install_requires=[
        'nltk ~= 3.3.0',
    ],
    entry_points={
        'console_scripts': ['csc=code_stat_collector:main'],
    },
)