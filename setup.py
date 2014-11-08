# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='Distutils',
    version='1.0',
    description='A Tornado based HTML to ePub service',
    long_description=('An RESTful service extract contents of HTML page, '
                 'transforms it into ePub file'
                 ' and sends it as email to a selected Kindle device'),
    author='Janusz Kowalczyk',
    author_email='kowalcj0@gmail.com',
    url='https://github.com/kowalcj0/dinky',
    license='MIT - see license.md',
    platform='Linux',
    packages=find_packages(exclude=['test']),
    entry_points={
        'console_scripts':
            ['dinky-srv = dinky.app:main']},
    )
