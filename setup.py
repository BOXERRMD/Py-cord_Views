from setuptools import setup

with open("README.md") as file:
    file = file.read()

setup(
    name="PycordViews",
    version="1.1.4",
    url="https://github.com/BOXERRMD/Py-cord_Views",
    author="Chronos (alias BOXERRMD)",
    author_email="vagabonwalybi@gmail.com",
    maintainer="Chronos",
    license="MIT License",
    description="Views for py-cord library",
    long_description=file,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.9"
    ],
    install_requires=[
        "py-cord==2.6.1"
    ],
    packages=['pycordViews', 'pycordViews/pagination', 'pycordViews/views', 'pycordViews/menu', 'pycordViews/multibot'],
    python_requires='>=3.9'
)