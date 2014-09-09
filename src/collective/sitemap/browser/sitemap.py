# -*- coding: utf-8 -*-
from BTrees.OOBTree import OOBTree
from DateTime import DateTime
from plone.app.layout.sitemap.sitemap import SiteMapView as BaseView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SiteMapIndexView(BaseView):
    """Creates the sitemap index
    """

    template = ViewPageTemplateFile('templates/sitemap_index.xml')

    def objects(self):
        """Returns the data to create the sitemap."""
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {}
        query['portal_type'] = 'Folder'
        query['path'] = {
            'query': '/'.join(self.context.getPhysicalPath()),
            'depth': 1,
        }

        # HACK
        lastmod = DateTime().ISO8601()
        yield {
            'loc': '{0}/sitemap-root.xml.gz'.format(self.context.absolute_url()),
            'lastmod': lastmod,
        }
        for item in catalog.searchResults(query, Language='all'):
            loc = item.getURL()
            yield {
                'loc': '{0}/sitemap.xml.gz'.format(loc),
                'lastmod': lastmod,
            }


class SiteMapView(BaseView):
    """Creates the sitemap as explained in the specifications.

    http://www.sitemaps.org/protocol.php
    """

    template = ViewPageTemplateFile('templates/sitemap.xml')


class SiteMapRootView(BaseView):
    """Creates the sitemap as explained in the specifications.

    http://www.sitemaps.org/protocol.php
    """

    template = ViewPageTemplateFile('templates/sitemap.xml')

    def objects(self):
        """Returns the data to create the sitemap."""
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {}
        utils = getToolByName(self.context, 'plone_utils')
        query['portal_type'] = utils.getUserFriendlyTypes()
        query['portal_type'].remove('Folder')
        ptool = getToolByName(self, 'portal_properties')
        siteProperties = getattr(ptool, 'site_properties')
        typesUseViewActionInListings = frozenset(
            siteProperties.getProperty('typesUseViewActionInListings', [])
        )

        query['path'] = {
            'query': '/'.join(self.context.getPhysicalPath()),
            'depth': 1,
        }

        query['is_default_page'] = True
        default_page_modified = OOBTree()
        for item in catalog.searchResults(query, Language='all'):
            key = item.getURL().rsplit('/', 1)[0]
            value = (item.modified.micros(), item.modified.ISO8601())
            default_page_modified[key] = value

        # The plone site root is not catalogued.
        loc = self.context.absolute_url()
        date = self.context.modified()
        # Comparison must be on GMT value
        modified = (date.micros(), date.ISO8601())
        default_modified = default_page_modified.get(loc, None)
        if default_modified is not None:
            modified = max(modified, default_modified)
        lastmod = modified[1]
        yield {
            'loc': loc,
            'lastmod': lastmod,
            # 'changefreq': 'always', # hourly/daily/weekly/monthly/yearly/never
            # 'prioriy': 0.5, # 0.0 to 1.0
        }

        query['is_default_page'] = False
        for item in catalog.searchResults(query, Language='all'):
            loc = item.getURL()
            date = item.modified
            # Comparison must be on GMT value
            modified = (date.micros(), date.ISO8601())
            default_modified = default_page_modified.get(loc, None)
            if default_modified is not None:
                modified = max(modified, default_modified)
            lastmod = modified[1]
            if item.portal_type in typesUseViewActionInListings:
                loc += '/view'
            yield {
                'loc': loc,
                'lastmod': lastmod,
                # 'changefreq': 'always', # hourly/daily/weekly/monthly/yearly/never
                # 'prioriy': 0.5, # 0.0 to 1.0
            }
