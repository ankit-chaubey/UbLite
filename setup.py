#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import os

os.system("python3 -m UbLite.setup_config")

setup(
    name="UbLite",
    version="0.1.0",
    author="Ankit Chaubey",
    author_email="m.ankitchaubey@gmail.com",
    description="A lightweight and efficient Telegram userbot for automation.",
    long_description="UbLite is a streamlined Telegram userbot designed for automation, featuring high efficiency, lightweight performance, and easy customization.",
    long_description_content_type="text/plain",
    url="https://github.com/ankit-chaubey/UbLite",
    packages=["UbLite"],
    install_requires=[
        'telethon',
        'colorama',
    ],
    entry_points={
        "console_scripts": [
            "ublite=UbLite.userbot:main",
            "ublite-config=UbLite.setup_config:main",
            "ublite-update=UbLite.update:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
