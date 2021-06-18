import os

import setuptools  # type:ignore

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(os.path.join('renderer', '__init__.py')) as f:
    for line in f:
        if line.strip().startswith('__version__'):
            VERSION = line.split('=')[1].strip()[1:-1].strip()
            break

setuptools.setup(
    name="homie",
    setup_requires=['setuptools_scm'],
    version=VERSION,
    author="Leon Morten Richter",
    author_email="github@leonmortenrichter.de",
    description="Simple single static site generator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/M0r13n/pyais",
    license="MIT",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["static", "site", "website", "jinja", "generator"],
    python_requires='>=3.6',
    install_requires=[
        "related",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            'homie=renderer.__main__:main'
        ]
    }
)