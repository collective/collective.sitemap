# -*- coding:utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.0a2.dev0'
description = 'Enhanced sitemaps.org protocol implementation for Plone.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='collective.sitemap',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plone sitemaps sitemap',
    author='Simples Consultoria',
    author_email='produtos@simplesconsultoria.com.br',
    url='https://github.com/collective/collective.sitemap',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'plone.app.upgrade',
        'Products.CMFPlone >=4.2',
        'Products.GenericSetup',
        'setuptools',
        'zope.i18nmessageid',
        'zope.interface',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot] >=4.2.2',
            'plone.browserlayer',
            'plone.testing',
            'robotsuite',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
