    #!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'python-levenshtein==0.12.0',
    'requests==2.25.0',
    'Click>=7.0',
    'collatex==2.2',
    'lxml==4.6.1',
    'pandas==1.1.5',
    'tqdm==4.52.0'
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
    long_description=readme + '\n\n' + history,
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
    version='1.1.0',
    zip_safe=False,
)
