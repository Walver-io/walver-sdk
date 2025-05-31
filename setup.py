#!/usr/bin/env python
"""
Setup script for the Python Walver sdk.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    "anyio==4.9.0",
    "certifi==2025.4.26", 
    "charset-normalizer==3.4.1",
    "h11==0.16.0",
    "httpcore==1.0.9",
    "httpx==0.28.1",
    "idna==3.10",
    "python-dotenv==1.1.0", 
    "requests==2.32.3",
    "sniffio==1.3.1",
    "urllib3==2.4.0"
]

setup(
    name="walver-sdk",
    version="0.0.9",
    author="BonifacioCalindoro",
    author_email="admin@walver.io",
    description="A comprehensive Python wrapper for the Walver API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/walver-io/walver-python-sdk",
    packages=find_packages(include=["walver_sdk", "walver_sdk.*"]),
    package_data={
        "walver_sdk": ["py.typed"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords=["walver", "api", "wrapper", "client", "wallet", "verification" "blockchain", "solana", "ethereum", "crypto", "tokengate"],
    include_package_data=True,
) 
