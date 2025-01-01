from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='openwebui_python',
    version='0.0.4',
    packages=find_packages(),
    install_requires=install_requires,
    description='A Python client for interacting with OpenWebUI\'s API, providing easy access to language models and chat completions.',
    author='John Provost',
    author_email='john@johnprovost.com',
    url='https://github.com/jprovolone/OpenWebUIAPI-Python',
)