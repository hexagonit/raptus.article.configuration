
# -*- coding: utf-8 -*-
"""Utilities for looking up placeful configuration for Components."""

from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from raptus.article.configuration.interfaces import IConfigurableArticle
from raptus.article.core.interfaces import IComponentsConfiguration
from zope.component import adapts
from zope.interface import implements


class PlacefulComponentsConfiguration(object):
    """Provides lookup of placeful Components configuration."""
    implements(IComponentsConfiguration)
    adapts(IConfigurableArticle)

    def __init__(self, context):
        self.context = context

    def get(self, key, default=None):
        """Find the configuration key by looking first on context, then on all
        parents in aquisition chain and lastly in portal_properties.
        """

        # is this configuration key placefully on context or on some parent
        # in the aquisition chain?
        objects = self.getAcqusitionChain(self.context)
        for obj in objects:
            if obj.hasProperty(key):
                return obj.getProperty(key, default)

        # as a fall-back, read configuration from portal_properties
        props = getToolByName(self.context, 'portal_properties').raptus_article
        return props.getProperty(key, default)

    def getAcqusitionChain(self, context):
        """Returns a list of all context's parents up until to the portal root.

        :param context: An Article
        :returns: Iterable of all parents from the direct parent to the site root
        """

        # It is important to use inner to bootstrap the traverse,
        # or otherwise we might get surprising parents
        # E.g. the context of the view has the view as the parent
        # unless inner is used
        obj = aq_inner(context)

        while obj is not None:
            yield obj

            if ISiteRoot.providedBy(obj):
                break

            obj = aq_parent(obj)
