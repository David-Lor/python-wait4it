from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="wait4it",
    py_modules=["wait4it"],
    version="0.2.1",
    license="ISC",
    description="Wait until a certain TCP port is available",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="David-Lor",
    author_email="17401854+David-Lor@users.noreply.github.com",
    url="https://github.com/David-Lor/python-wait4it/",
    download_url="https://github.com/David-Lor/python-wait4it/archive/master.zip",
    keywords=["tcp", "wait-for-it"],
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ]
)
