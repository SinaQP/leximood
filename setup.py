from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="leximood",
    version="0.1.0",
    author="LexiMood Team",
    author_email="info@leximood.com",
    description="A Persian sentiment analysis library for text emotion detection",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/leximood/leximood",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
    },
    include_package_data=True,
    package_data={
        "leximood": ["data/*.json", "data/*.txt"],
    },
    keywords="persian sentiment analysis nlp text processing emotion detection",
    project_urls={
        "Bug Reports": "https://github.com/leximood/leximood/issues",
        "Source": "https://github.com/leximood/leximood",
        "Documentation": "https://leximood.readthedocs.io/",
    },
) 