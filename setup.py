from setuptools import setup, find_packages

setup(
    name='KrakenPythonMarcosRodrigo',
    version='0.1.0',
    packages=find_packages(),
    description='A streamlit tool for rendering kraken data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Marcos Castro Cacho & Rodrigo de la Nuez Moraleda',
    author_email='mcastrocach@alumni.unav.es',
    url='https://github.com/mcastrocach/ppad',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)