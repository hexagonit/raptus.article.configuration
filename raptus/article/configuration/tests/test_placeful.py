# -*- coding: utf-8 -*-
"""Testing placeful configuration."""

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from Products.CMFCore.utils import getToolByName
from raptus.article.configuration.tests.base import RAConfigurationIntegrationTestCase
from raptus.article.configuration.interfaces import IConfigurableArticle

import unittest2 as unittest


class TestGetAcqusitionChain(RAConfigurationIntegrationTestCase):
    """Test getting aquisition chain of content objects."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        # allow adding Subarticles to Articles
        portal_types = getToolByName(self.portal, 'portal_types')
        types = list(portal_types.Article.allowed_content_types)
        types.append('Article')
        portal_types.Article.allowed_content_types = tuple(types)

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article', title='Räptus Articlë')
        self.portal.article.invokeFactory('Article', 'subarticle', title='Räptus Subarticlë')
        self.portal.article.subarticle.invokeFactory('Article', 'subsubarticle', title='Räptus Subsubarticlë')

    def makePlacefulComponentsConfiguration(self, context):
        """Make an instance of PlacefulComponentsConfiguration"""
        from raptus.article.configuration.placeful import PlacefulComponentsConfiguration
        return PlacefulComponentsConfiguration(context)

    def test_first_level_article(self):
        """Test that top-level Article has only itself in its acquisition
        chain.
        """
        configuration = self.makePlacefulComponentsConfiguration(self.portal.article)
        objects = configuration.getAcqusitionChain()
        self.assertEquals('article'.split(), [o.id for o in objects])

    def test_second_level_article(self):
        """Test that second-level Article has itself and its parent
        in its acquisition chain."""
        configuration = self.makePlacefulComponentsConfiguration(self.portal.article.subarticle)
        objects = configuration.getAcqusitionChain()
        self.assertEquals('subarticle article'.split(), [o.id for o in objects])

    def test_third_level_article(self):
        """Test that third-level Article has itself and all its parents
        in its acquisition chain."""
        configuration = self.makePlacefulComponentsConfiguration(self.portal.article.subarticle.subsubarticle)
        objects = configuration.getAcqusitionChain()
        self.assertEquals('subsubarticle subarticle article'.split(), [o.id for o in objects])


class TestIConfigurableArticle(RAConfigurationIntegrationTestCase):
    """Test IConfigurableArticle is implemented by Article."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article', title='Räptus Articlë')

    def test_article_implements_configurable(self):
        """Test that Article implements IConfigurableArticle."""
        self.assertTrue(IConfigurableArticle.providedBy(self.portal.article))


class TestInstall(RAConfigurationIntegrationTestCase):
    """Test installation of raptus.article.configuration into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_product_installed(self):
        """Test if raptus.article.configuration is installed with
        portal_quickinstaller.
        """

        qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('raptus.article.configuration'))


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
