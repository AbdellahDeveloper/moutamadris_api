from setuptools import setup, find_packages

setup(
    name='moutamadris_api',
    version='1.0',
    packages=find_packages(),
    install_requires=['requests>=2.32.3', 'beautifulsoup4>=4.12.3'],
    author="Abdellah Elidrissi",
    description="This package provides an interface for interacting with the Moutamadris API. Moutamadris is a platform used by Moroccan students to access educational resources, track academic progress, and manage their accounts. This package allows developers to programmatically access these features, making it easier to integrate Moutamadris functionalities into their own applications.",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown'
)