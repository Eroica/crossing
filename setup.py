from distutils.core import setup

setup(
    name = 'crossing',
    version = '0.1.0',
    author = ['Dennis Ulmer', 'Sebastian Spaar'],
    author_email  = ['d.ulmer@stud.uni-heidelberg.de', 'spaar@stud.uni-heidelberg.de'],
    packages = ['crossing'],
    scripts = [],
    url = 'https://github.com/Eroica/crossing',
    license = 'LICENSE.txt',
    description = 'crossing can create transformation matrices using a provided dictionary and two language model files.',
    long_description = open('README.txt').read(),
    install_requires = [
        "numpy",
        "scipy",
        "scikit-learn",
        "nose",
        "beautiful-soup",
    ],
)