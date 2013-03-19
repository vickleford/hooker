try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Hooks up a new agent to a puppetmaster',
    'author': 'Vickleford',
    'url': 'https://github.com/vickleford/hooker',
    'download_url': 'https://github.com/vickleford/hooker',
    'author_email': 'vwatkinsjr@gmail.com',
    'version': '0.1',
    'install_requires': ['paramiko', 'getpass', 'configobj', 'keyring'],
    'packages': ['hooker'],
    'name': 'hooker',
    'entry_points': {
        'console_scripts': [
            'hooker = hooker.script:main',
            'hooker-passwd = hooker.script.set_password'
        ]
    }
}

setup(**config)