
from setuptools import setup, find_packages
from tetrationcli.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='tetrationcli',
    version=VERSION,
    description='Getting basic interactions with Tetration via our favourite media, the cli',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Julio Molina Soler',
    author_email='jmolinas@cisco.com',
    url='https://github.com/jumolinas/tetrationcli',
    license='MIT License',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'tetrationcli': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        tetrationcli = tetrationcli.main:main
    """,
)
