#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()


requirements = [
    'acdh-tei-pyutils>=0.25.0,<1',
    'beautifulsoup4>=4.11.1,<5',
    'click>=7.1<9',
    'collatex==2.2',
    'pandas>=1.1.5,<2',
    'python-Levenshtein',
    'tqdm>=4.52.0,<5'
]

setup_requirements = []

test_requirements = []

setup(
    author="Peter Andorfer",
    author_email='peter.andorfer@oeaw.ac.at',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    description="Utility functions to work with collatex",
    entry_points={
        'console_scripts': [
            'collate=acdh_collatex_utils.cli:collate',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={
        '': ['fixtures/*.*'],
        'acdh_collatex_utils': ['xslt/*.xsl']
    },
    keywords='acdh_collatex_utils',
    name='acdh_collatex_utils',
    packages=find_packages(include=['acdh_collatex_utils', 'acdh_collatex_utils.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/acdh-oeaw/acdh_collatex_utils',
    version='1.11.0',
    zip_safe=False,
)
