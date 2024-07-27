from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='bushido',
    version='0.1.0',
    author='Noe Javet',
    description='tracking app',
    packages=find_packages(),
    package_data={
        'bushido': ['assets/*.tcss'],
    },
    install_requires=requirements
)

