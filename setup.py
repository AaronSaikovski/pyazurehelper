from setuptools import find_packages, setup

with open("app/README.md", "r") as fh:
    long_description = fh.read()

REQUIREMENTS = [   
    "azure-cli",
    "azure-cli-core",
    "azure-core",
    "azure-identity",
    "azure-common"
]

DEV_REQUIREMENTS = [
    "azure-cli",
    "azure-cli-core",
    "azure-core",
    "azure-identity",
    "azure-common"
    "mypy",
    "ruff",
    "pytest"
]

setup(
    name="PyAzureToolkit",
    version="0.0.1",
    description="Python Azure Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AaronSaikovski/pyazuretoolkit",
    author="asaikovski",
    author_email="asaikovski@outlook.com",
    license="MIT",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    extras_require={
        "dev": DEV_REQUIREMENTS,
    },
    python_requires=">=3.11",
)
