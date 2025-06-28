# For setting up a Python package for a machine learning project
# This file is used to package the project and its dependencies
# It includes metadata about the package and lists the required dependencies

from setuptools import setup, find_packages
from typing import List

# Function to read requirements from a file to a list
def get_requirements(file_path: str) -> List[str]:
    requirements = []

    # \n is used to split the lines in the requirements file
    # We read the file and remove any newline characters
    with open('requirements.txt', 'r') as file:
        requirements = file.readlines()
        requirements = [req.replace('\n', '') for req in requirements]

    # -e . is a common way to specify the current directory as a package
    # We remove it from the requirements list if it exists
        if '-e .' in requirements:
            requirements.remove('-e .')
    return requirements

setup(
    name='mlproject',
    version='0.1.0',
    author='Mak',
    author_email='akshay.nitt04@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'scikit-learn',
    ]
)