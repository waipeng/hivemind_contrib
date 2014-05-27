#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='hivemind_contrib',
    version='0.1',
    description='Python Boilerplate contains all the boilerplate you need to create a Python package.',
    long_description=readme + '\n\n' + history,
    author='Russell Sim',
    author_email='russell.sim@gmail.com',
    url='https://github.com/russell/hivemind_contrib',
    packages=[
        'hivemind_contrib',
    ],
    package_dir={'hivemind_contrib':
                 'hivemind_contrib'},
    include_package_data=True,
    install_requires=requirements,
    license="GPLv2",
    zip_safe=False,
    keywords='hivemind_contrib',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
    tests_require=test_requirements,
      entry_points="""
      # -*- Entry points: -*-

      [hivemind.modules]
      iptables = hivemind_contrib.iptables
      libvirt = hivemind_contrib.libvirt
      nectar = hivemind_contrib.nectar
      nova = hivemind_contrib.nova
      gerrit = hivemind_contrib.gerrit
      packages = hivemind_contrib.packages
      packaging = hivemind_contrib.packaging
      pbuilder = hivemind_contrib.pbuilder
      repo = hivemind_contrib.repo
      swift = hivemind_contrib.swift
      """,
)
