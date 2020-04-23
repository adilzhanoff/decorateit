from setuptools import setup, find_packages


__NAME: str = 'decorateit'

__VERSION: str = '0.0.1a1'

__AUTHOR: str = 'Rasul Adilzhanov'

__AUTHOR_EMAIL: str = 'rasuladilzhanoff@gmail.com'

__DESCRIPTION: str = (
    "Simple but extremely useful package that " +
    "provides great decorators for your programs"
)

with open("README.md", "r") as fh:
    __LONG_DESCRIPTION: str = fh.read()

__LONG_DESCRIPTION_CONTENT_TYPE: str = 'text/markdown'

__URL: str = 'https://github.com/adilzhanoff/decorateit'

__PACKAGES: list = find_packages()

__LICENSE: str = 'GPLv3+'

__LICENSE_CLASS: str = (
    "License :: OSI Approved :: GNU General " +
    "Public License v3 or later (GPLv3+)"
)

__CLASSIFIERS: list = [
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    __LICENSE_CLASS,
    "Operating System :: OS Independent",
]

setup(
    name=__NAME,
    version=__VERSION,
    author=__AUTHOR,
    author_email=__AUTHOR_EMAIL,
    description=__DESCRIPTION,
    long_description=__LONG_DESCRIPTION,
    long_description_content_type=__LONG_DESCRIPTION_CONTENT_TYPE,
    url=__URL,
    packages=__PACKAGES,
    license=__LICENSE,
    classifiers=__CLASSIFIERS,
    python_requires='>=3.6',
)
