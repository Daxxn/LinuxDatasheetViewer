from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="Datasheets",
    version="1.0.0",
    author="Daxxn Lantz",
    author_email="nynjalantz@gmail.com",
    description="An application to manage and search for electrical datasheets.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Daxxn/LinuxDatasheetViewer/",
    packages=find_packages(),
    install_requires=[],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
        "Topic :: Desktop Environment :: Gnome"
    ],
    fullname="Datasheet manager"
)