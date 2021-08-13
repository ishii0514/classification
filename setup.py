import os
from setuptools import setup, find_packages


def read_requirements():
    req_path = os.path.join('.', 'requirements.txt')
    with open(req_path, 'r') as f:
        reqs = [l.rstrip() for l in f]
    return reqs


setup(
    name='classification',
    version='0.0.1',
    description='Classify image.',
    author='Ishii Yosuke',
    install_requires=read_requirements(),
    license=license,
    packages=find_packages(exclude=('tests')),
    entry_points={
        'console_scripts': [
            'classification=classification.__main__:main'
        ]
    }
)
