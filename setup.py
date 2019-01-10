"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='team94_robot_2019',  # Required
    version='0.0.1',  # Required
    maintainer='Aaron DeGrow',
    maintainer_email='ninetyfouriors@gmail.com',
    description='NinetyFouriors Team 94 robot code',  # Required
    long_description=long_description,  # Optional
    url='https://github.com/TechnoJays/robot2019',  # Optional
    classifiers=[  # Optional
        'Development Status :: 4 - Beta',
        'Environment :: roboRIO'
        'Intended Audience :: Developers',
        'Topic :: FIRST FRC :: Team 94 Robot Code',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='first team94 roboPy',  # Optional
    packages=find_packages(exclude=["tests/*"]),  # Required
    install_requires=['pyfrc'],  # Optional
    extras_require={  # Optional
        'test': ['tox', 'coverage'],
    }
)
