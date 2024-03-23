from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='skynet',
    version='0.0.0',
    author='Noe Javet',
    packages=find_packages(),
    install_requires=requirements
)
