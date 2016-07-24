from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys
import re
import ast
import os


def read(filename):
    with open(filename, 'r') as fh:
        return fh.read()


class ToxTest(TestCommand):
    user_options = [('tox-args=', 'a', 'Arguments to pass to tox')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        args = []
        if self.tox_args:
            args = shlex.split(self.tox_args)

        errno = tox.cmdline(args=args)
        sys.exit(errno)


if __name__ == "__main__":
    setup(
        name='datestuff',
        version='0.1.0',
        author='Alec Nikolas Reiter',
        author_email='alecreiter@gmail.com',
        description='Stuff for dates',
        long_description=read('README.rst'),
        license='MIT',
        packages=['datestuff'],
        zip_safe=False,
        url="https://github.com/justanr/datestuff",
        keywords=['dates'],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Topic :: Utilities',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5'
        ],
        test_suite='test',
        tests_require=['tox'],
        cmdclass={'tox': ToxTest},
    )
