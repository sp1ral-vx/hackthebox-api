from setuptools import setup, find_packages

VERSION = '0.0.1'
setup(
    name='hackthebox-api',
    packages=find_packages(),
    version=VERSION,
    description='Unofficial hackthebox.eu API wrapper and CLI application.',
    author='Sp1ral',
    url='https://github.com/sp1ral-vx/hackthebox-api',
    download_url='https://github.com/sp1ral-vx/hackthebox-api/tarball/' + VERSION,
    keywords=['hackthebox', 'htb'],
    classifiers=[],
    scripts=['bin/hackthebox.py'],
    python_requires='>=3.5',
    install_requires=[
        'beautifulsoup4==4.8.1',
        'bs4==0.0.1',
        'certifi==2019.9.11',
        'chardet==3.0.4',
        'colorama==0.4.1',
        'idna==2.8',
        'prettytable==0.7.2',
        'Pysher==1.0.4',
        'requests==2.22.0',
        'six==1.13.0',
        'soupsieve==1.9.5',
        'urllib3==1.25.6',
        'websocket-client==0.56.0',
    ],
)
