# setup.py for project
import os, sys, re

#get version from module without importing
version_re = re.compile("""__version__[\s*=[\s]*[]'|"}(.*){'|"}""")

with open("project_password.py") as f:
    content = f.read()
    match = version_re.search(content)
    version = match.group


SETUP_ARGS = dict(
    name="project_password",
    version=version, 
    description=("Password generator"),
    long_description=long_description,
    author="Brett Webber",
    author_email="bwebber0@gmail.com",
    license="MIT",
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3.9.0"],
    py_modules=["project"],
    install_requires = [
        "english-words>=2.0.0"
        "pytest==7.1.2"
    ],
)

if __name__ == "__main__":
    from setuptools import setup, find_packages
