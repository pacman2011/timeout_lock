#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import setuptools


def read(*paths):
    with open(os.path.join(*paths), "r") as filename:
        return filename.read()


def main():
    setuptools.setup(
        name             = "timeout_lock",
        version          = "1.0_2019-04-08",
        description      = "Control lock with Timeout on acquire",
        long_description = (read("README.rst")),
        url              = "https://github.com/pacman2011/timeout_lock",
        author           = "Shane Boissevain",
        author_email     = "shaneboissevain@gmail.com",
        license          = "GPLv3",
        py_modules       = ["timeout_lock"],
    )


if __name__ == "__main__":
    main()
