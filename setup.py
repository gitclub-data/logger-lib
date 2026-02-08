from setuptools import setup, find_packages

setup(
    name="logger-lib",
    version="0.1.0",
    description="Plug and play logging module with rich functionalities",
    author="Gaurav Pandey",
    author_email="gauravpandey1207@gmail.com",
    packages=find_packages(include=["logger", "logger.*"]),
    install_requires=[
        "typing-extensions>=4.0.0",
        "tzdata>=2023.3"
    ],
    python_requires=">=3.7",
)
