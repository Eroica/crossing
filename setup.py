from distutils.core import setup

setup(
    name = 'crossing',
    version = '0.1.0',
    author = 'J. Random Hacker',
    author_email  = 'jrh@example.com',
    packages = ['towelstuff', 'towelstuff.test'],
    scripts = ['bin/stowe-towels.py','bin/wash-towels.py'],
    url = 'http://pypi.python.org/pypi/TowelStuff/',
    license = 'LICENSE.txt',
    description = 'Useful towel-related stuff.',
    long_description = open('README.txt').read(),
    install_requires = [
        "numpy",
        "scipy",
        "scikit-learn",
    ],
)