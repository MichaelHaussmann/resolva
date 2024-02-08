# -*- coding: utf-8 -*-

"""
This is a package definition for rez.
https://github.com/AcademySoftwareFoundation/rez
https://rez.readthedocs.io
"""

name = 'resolva'

version = '0.1.0'

requires = []

description = "https://github.com/MichaelHaussmann/resolva"
authors = ['Michael Haussmann']


def commands():
    env.PYTHONPATH.append('{root}')


is_pure_python = True
