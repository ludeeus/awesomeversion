"""The setup script."""
from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Ludeeus",
    author_email="hi@ludeeus.dev",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="One version package to rule them all, One version package to find them, One version package to bring them all, and in the darkness bind them.",
    keywords=["calver", "semver", "0ver", "version", "buildver"],
    license="MIT license",
    long_description_content_type="text/markdown",
    long_description=readme,
    name="awesomeversion",
    python_requires=">=3.7",
    packages=find_packages(include=["awesomeversion", "awesomeversion.*"]),
    package_data={"awesomeversion": ["py.typed"]},
    url="https://github.com/ludeeus/awesomeversion",
    version="main",
)
