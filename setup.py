"""Configure the distribution of the package."""

from setuptools import setup

setup(
    name="word_graph",
    version="0.0.1",
    packages=["word_graph"],
    entry_points={
        'console_scripts': [
            'word-graph=word_graph.main:main',
        ],
    },
    install_requires=[
        "argparse",
        "pytest"
    ],
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    license="MIT"
)
