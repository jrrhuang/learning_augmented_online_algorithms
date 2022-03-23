# coding=utf-8
"""
Setup for learning_augmented_online_algorithms.
"""

import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="learning_augmented_online_algorithms",
    version="0.0.1",
    author="Jerry Huang",
    author_email="jrr.huang8@gmail.com",
    description="implementation of robustness guarantees in learning algorithms papers. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={"": ["LICENSE.txt"]},
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "datetime",
        "pandas",
        "numpy"
    ],
)