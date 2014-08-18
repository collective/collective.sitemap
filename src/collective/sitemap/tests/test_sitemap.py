# -*- coding: utf-8 -*-
from collective.sitemap.interfaces import IBrowserLayer
from collective.sitemap.testing import FUNCTIONAL_TESTING
from gzip import GzipFile
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing.z2 import Browser
from StringIO import StringIO
from zope.interface.declarations import directlyProvides

import transaction
import unittest


class BaseTestCase(unittest.TestCase):
    """Base test case to be used by other tests."""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.wt = self.portal['portal_workflow']
        self.request = self.layer['request']
        directlyProvides(self.request, IBrowserLayer)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.browser = Browser(app)
        self.wt.setChainForPortalTypes(['Document', 'Event', 'Folder', 'News Item'],
                                       ['simple_publication_workflow'],)
        self.setup_content()
        transaction.commit()

    def setup_content(self):
        portal = self.portal
        contents = []
        contents.append(api.content.create(type='Folder', title='News', container=portal))
        contents.append(api.content.create(type='News Item',
                                           title='News 1',
                                           container=portal['news']))
        contents.append(api.content.create(type='News Item',
                                           title='News 2',
                                           container=portal['news']))
        contents.append(api.content.create(type='News Item',
                                           title='News 3',
                                           container=portal['news']))
        contents.append(api.content.create(type='Folder', title='Events', container=portal))
        contents.append(api.content.create(type='Event',
                                           title='First Event',
                                           container=portal['events']))
        contents.append(api.content.create(type='Event',
                                           title='Second Event',
                                           container=portal['events']))
        contents.append(api.content.create(type='Folder', title='Blogs', container=portal))
        contents.append(api.content.create(type='Folder',
                                           title='Our Blog',
                                           container=portal['blogs']))
        contents.append(api.content.create(type='Folder',
                                           title='Another Blog',
                                           container=portal['blogs']))
        contents.append(api.content.create(type='Document', title='About Us', container=portal))
        for content in contents:
            api.content.transition(obj=content, transition='publish')

    def uncompress(self, sitemapdata):
        sio = StringIO(sitemapdata)
        unziped = GzipFile(fileobj=sio)
        xml = unziped.read()
        unziped.close()
        return xml

    def test_sitemap_index_available(self):
        browser = self.browser
        browser.open('%s/sitemap.xml.gz' % self.portal.absolute_url())
        self.assertEqual(browser.headers['status'], '200 Ok')
        self.assertEqual(browser.headers['content-type'], 'application/octet-stream')

    def test_sitemap_index_content(self):
        browser = self.browser
        browser.open('%s/sitemap.xml.gz' % self.portal.absolute_url())
        data = self.uncompress(browser.contents)
        self.assertIn('<loc>http://nohost/plone/sitemap-root.xml.gz</loc>', data)
        self.assertIn('<loc>http://nohost/plone/blogs/sitemap.xml.gz</loc>', data)
        self.assertIn('<loc>http://nohost/plone/events/sitemap.xml.gz</loc>', data)
        self.assertIn('<loc>http://nohost/plone/news/sitemap.xml.gz</loc>', data)

    def test_sitemap_root_available(self):
        browser = self.browser
        browser.open('%s/sitemap-root.xml.gz' % self.portal.absolute_url())
        self.assertEqual(browser.headers['status'], '200 Ok')
        self.assertEqual(browser.headers['content-type'], 'application/octet-stream')

    def test_sitemap_root_content(self):
        browser = self.browser
        browser.open('%s/sitemap-root.xml.gz' % self.portal.absolute_url())
        data = self.uncompress(browser.contents)
        self.assertIn('<loc>http://nohost/plone/about-us</loc>', data)

    def test_sitemap_folder(self):
        browser = self.browser
        # News folder
        browser.open('%s/sitemap.xml.gz' % self.portal['news'].absolute_url())

        self.assertEqual(browser.headers['status'], '200 Ok')
        self.assertEqual(browser.headers['content-type'], 'application/octet-stream')

        data = self.uncompress(browser.contents)
        self.assertIn('<loc>http://nohost/plone/news/news-1</loc>', data)
        self.assertIn('<loc>http://nohost/plone/news/news-2</loc>', data)
        self.assertIn('<loc>http://nohost/plone/news/news-3</loc>', data)
