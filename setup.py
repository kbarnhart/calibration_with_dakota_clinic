#! /usr/bin/env python
from setuptools import setup, find_packages


setup(
    name="heat",
    author="Katy Barnhart/Eric Hutton",
    author_email="eric.hutton@colorado.edu",
    description="1D heat model",
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    install_requires=["bmipy", "pyyaml", "scipy"],
    packages=find_packages(),
)
