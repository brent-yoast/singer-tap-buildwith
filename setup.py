#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-buildwith",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_buildwith"],
    install_requires=[
        # NB: Pin these to a more specific version for tap reliability
        "singer-python",
        "requests",
    ],
    entry_points="""
    [console_scripts]
    tap-buildwith=tap_buildwith:main
    """,
    packages=["tap_buildwith"],
    package_data = {
        "schemas": ["tap_buildwith/schemas/*.json"]
    },
    include_package_data=True,
)
