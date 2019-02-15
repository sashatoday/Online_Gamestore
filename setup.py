from setuptools import setup, find_packages

setup(
    name="wsd",
    version="0.1",
    packages=find_packages(),
    scripts=[],

    install_requires=['docutils>=0.3'],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md'],
    },

    # metadata for upload to PyPI
    author="",
    author_email="",
    description="",
    license="MIT",
    keywords="",
    url="",   # project home page

)