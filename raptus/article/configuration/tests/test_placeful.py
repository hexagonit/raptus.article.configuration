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

    def makePlacefulComponentsConfiguration(self):
        """Make an instance of PlacefulComponentsConfiguration"""
        from raptus.article.core.componentfilter import ComponentFilter
        context = mock.sentinel.context
        request = mock.sentinel.request
        view = mock.sentinel.view
        return ComponentFilter(context, request, view)

    def test_first_level_article(self):
        """Test that Article implements IConfigurableArticle."""
        self.assertTrue(IConfigurableArticle.providedBy(self.portal.article))


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
