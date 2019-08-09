from setuptools import setup

setup(
    name='python-todo',
    version='0.1',
    description='A command line todo application',
    url='http://github.com/weaverdyl/python-todo',
    author='Dylan Weaver',
    author_email='dylan@weaverdyl.compile',
    license='MIT',
    packages=['todo_app'],
    entry_points={
          "console_scripts": [
              'python-todo = todo_app.todo:run'
          ]
    },
    zip_safe=False)
