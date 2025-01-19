from setuptools import setup, find_packages

setup(
    name="pipecat",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "deepgram-sdk>=3.0.0",
        "loguru",
        "python-dotenv",
    ],
)
