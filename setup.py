import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


install_requires = [
    "google-auth==2.0.2",
    "Jinja2==3.0.1",
    "pandas>=1.3.2",
    "google-api-python-client==2.20.0",
    "google-auth-httplib2==0.1.0",
    "google-auth-oauthlib==0.4.6",
    "pytest==6.2.5",
    "google-cloud-storage==1.42.2",
    "google-cloud-pubsub==2.8.0",
]


setup(
    name="aspen",
    version="0.0.3",
    author="Ethan Lyon",
    author_email="ethanl@seerinteractive.com",
    description=("A simple library to read and write data."),
    packages=find_packages(),
    license="MIT",
    keywords="etl",
    install_requires=install_requires,
    long_description=read("README.md"),
    entry_points={"console_scripts": ["aspen = aspen.cli.cli:main"]},
)
