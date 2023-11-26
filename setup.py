from setuptools import setup, find_packages
from appdirs import user_cache_dir, user_config_dir
from glob import glob
import os


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

"""
cache_dir = user_cache_dir('textile')
config_dir = user_config_dir('textile')

cache_file = glob(os.path.join('cache', '*.csv'))

data_files = [
    (cache_dir, cache_file),
    (config_dir, ['./config/config.init']),
]
"""

setup(
    name='textile',
    version='1.0.0',
    maintainer='salaheddine.ghamri@yahoo.com',
    packages=find_packages(),
    include_package_data=True,
    long_description=open('README.md').read(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'textile = textile:main',
        ],
    },
)
