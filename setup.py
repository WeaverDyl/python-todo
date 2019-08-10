from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-todo',
    version='0.4',
    description='A command line todo application',
    long_description = long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'terminaltables',
    ],
    url='http://github.com/weaverdyl/python-todo',
    author='Dylan Weaver',
    author_email='dylan@weaverdyl.com',
    license='MIT',
    packages=['todo_app'],
    entry_points={
          "console_scripts": [
              'python-todo = todo_app.todo:run'
          ]
    },
    zip_safe=False)
