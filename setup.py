from pathlib import Path
from setuptools import setup

_classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
]


def _version():
    with open('kson/__init__.py') as fp:
        line = next(i for i in fp if i.startswith('__version__'))
        return line.strip().split()[-1].strip("'")


if __name__ == '__main__':
    VERSION = _version()
    if False:
        REQUIREMENTS = Path('requirements.txt').read_text().splitlines()
    else:
        REQUIREMENTS = []

    setup(
        name='kson',
        version=VERSION,
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        url='https://github.com/rec/kson',
        py_modules=['kson'],
        description='KSON is JSON with the bad parts fixed',
        long_description=open('README.rst').read(),
        license='MIT',
        classifiers=_classifiers,
        keywords=['JSON', 'data', 'serialization', ],
        install_requires=REQUIREMENTS,
    )
