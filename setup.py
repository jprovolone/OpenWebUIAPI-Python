from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='openwebui_python',
    version='0.1.0',  # Updated version to reflect the refactoring
    packages=find_packages(),
    install_requires=install_requires,
    description='A professionally organized Python SDK for interacting with OpenWebUI\'s API, providing easy access to language models, chat completions, files, knowledge bases, and more.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='John Provost',
    author_email='john@johnprovost.com',
    url='https://github.com/jprovolone/OpenWebUIAPI-Python',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    keywords='openwebui, api, sdk, llm, language model, chat',
)
