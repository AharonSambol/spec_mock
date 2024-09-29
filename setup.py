from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="spec_mock",
    version="1.0.1",
    author="Aharon Sambol",
    author_email="aharon.sambol@gmail.com",
    py_modules=find_packages("spec_mock"),
    packages=find_packages(),
    license="MIT License",
    url="https://github.com/AharonSambol/spec_mock",
    keywords=["mock", "spec", "test"],
    description="Powerful mocks with complete specs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
)
