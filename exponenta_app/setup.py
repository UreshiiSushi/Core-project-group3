from setuptools import setup, find_namespace_packages

setup(
    name='exponenta-app',
    version='0.1.5',
    description='Helper for address book, notebook, sorting files',
    url='https://github.com/UreshiiSushi/Exponenta-app',
    author='PythonCore18-group3',
    license='MIT',
    packages=find_namespace_packages(),
    #py_modules=['exponenta_app.exponenta_main', 'exponenta_app.modules.address_book', 'exponenta_app.modules.note', 'exponenta_app.modules.sort'],
    install_requires=['prompt-toolkit'],
    entry_points = {'console_scripts': ['exponenta-app=exponenta_app.exponenta_main:main']}
    )