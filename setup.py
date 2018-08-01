from setuptools import find_packages, setup


def read(filename):
    with open(filename, "r") as fh:
        return fh.read()


def long_descript():
    return "\n\n".join([read(f) for f in ("README.rst", "LICENSE")])


if __name__ == "__main__":
    setup(
        name="datestuff",
        version="0.3.0",
        author="Alec Nikolas Reiter",
        author_email="alecreiter@gmail.com",
        description="Stuff for dates",
        long_description=long_descript(),
        license="MIT",
        packages=find_packages("src", exclude=["test"]),
        package_dir={"": "src"},
        include_package_data=True,
        package_data={"": ["LICENSE", "README.rst", "CHANGELOG"]},
        zip_safe=False,
        url="https://github.com/justanr/datestuff",
        keywords=["dates", "datetime"],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Utilities",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
        ],
    )
