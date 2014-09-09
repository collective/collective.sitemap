***************************************************************
`collective.sitemap`
***************************************************************

.. contents:: Contents
   :depth: 2

Life, the Universe, and Everything
----------------------------------

``collective.sitemap`` is a package that implements a sitemap index according to `Sitemaps Specification <http://www.sitemaps.org/>`_.

Use cases
^^^^^^^^^

For sites and portals with more than 50,000 content items, the default sitemap implementation in Plone (available at plone.app.layout) will fail the constraints imposed by the protocol.
This package addresses that by replacing the default /sitemap.xml.gz in site root by a sitemap index, listing sitemaps for all folders under site root.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/collective/collective.sitemap.png?branch=master
    :alt: Travis CI badge
    :target: http://travis-ci.org/collective/collective.sitemap

.. image:: https://coveralls.io/repos/collective/collective.sitemap/badge.png?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/r/collective/collective.sitemap

.. image:: https://pypip.in/d/collective.sitemap/badge.png
    :alt: Downloads
    :target: https://pypi.python.org/pypi/collective.sitemap

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/collective.sitemap/issues


Installation
^^^^^^^^^^^^

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it::

    [buildout]
    ...
    eggs =
        collective.sitemap


After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.sitemap`` and click the 'Activate' button.
