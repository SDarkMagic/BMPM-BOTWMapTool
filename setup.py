import setuptools

with open("README.md", "r") as desc:
    long_description = desc.read()

setuptools.setup(
    name="BMPM",
    version="1.4.3",
    author="SDarkMagic",
    author_email="TheSDarkMagic@gmail.com",
    description="A program for bulk replacement of BYML map file parameters.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SDarkMagic/BMPM",
    packages=['bmpm'],
#    package_dir={'bmpm': 'scripts'},
    entry_points={
        'console_scripts': ['bmpm=bmpm.__main__:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "oead>=1.1.1",
    ],
)