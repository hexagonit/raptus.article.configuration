
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

import logging

logger = logging.getLogger('raptus.article.configuration')


class PlacefulComponentsConfiguration(object):
    """Provides lookup of placeful Components configuration."""
    implements(IComponentsConfiguration)
    adapts(IConfigurableArticle)

    def __init__(self, context):
        self.context = context

    def get(self, key, default=None):
        """Find the configuration key by looking first on context, then on all
        parents in acquisition chain and lastly in portal_properties.
        """
        # is this configuration key placefully on context or on some parent
        # in the aquisition chain?
        objects = self.getAcquisitionChain()
        for obj in objects:
            if obj.hasProperty(key):
                logger.debug("Read configuration for %s from %s." % (key, obj.absolute_url_path()))
                return obj.getProperty(key, default)

        # as a fall-back, read configuration from portal_properties
        props = getToolByName(self.context, 'portal_properties').raptus_article
        logger.debug("Read configuration for %s from portal_properties." % key)
        return props.getProperty(key, default)

    def getAcquisitionChain(self):
        """Returns a list of all context's parents up until to the portal root.

        :returns: Iterable of all parents from the direct parent to the site root
        :return type: generator
        """

        # It is important to use aq_inner to bootstrap the traverse,
        # otherwise we might get surprising parents
        # E.g. the context of the view has the view as the parent
        # unless aq_inner is used
        obj = aq_inner(self.context)

        while obj is not None:

            if ISiteRoot.providedBy(obj):
                break

            yield obj
            obj = aq_parent(obj)
