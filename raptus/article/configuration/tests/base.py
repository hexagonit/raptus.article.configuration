# -*- coding: utf-8 -*-
"""Layers and TestCases for our tests."""

from __future__ import with_statement

import unittest2 as unittest

from plone.testing import z2
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE


class RaptusArticleConfigurationLayer(PloneSandboxLayer):
    """Layer for Raptus Article Configuration tests."""

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import raptus.article.configuration
        self.loadZCML(package=raptus.article.configuration)
        z2.installProduct(app, 'raptus.article.configuration')
        z2.installProduct(app, 'raptus.article.core')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'raptus.article.configuration:default')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'raptus.article.configuration')


# FIXTURES
RAPTUS_ARTICLE_CONFIGURATION_FIXTURE = RaptusArticleConfigurationLayer()

# LAYERS
INTEGRATION_TESTING = IntegrationTesting(
    bases=(RAPTUS_ARTICLE_CONFIGURATION_FIXTURE, ),
    name="raptus.article.configuration:Integration")


# TESTCASES
class RAConfigurationIntegrationTestCase(unittest.TestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit
    test cases.
    """
    layer = INTEGRATION_TESTING
