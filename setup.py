#!/usr/bin/env python

import setuptools

from memsource import version


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="memsource",
    version=version.__version__,
    author="Yanis Guenane",
    author_email="yguenane+opensource@gmail.com",
    description="Python bindings for Memsource",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Spredzy/python-memsource",
    packages=setuptools.find_packages(),
    install_requires = [
        "requests"
    ]
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)
