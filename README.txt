Introduction
============

Provides placeful configuration for components.

The following features for raptus.article are provided by this package:

Interfaces
----------
    * IConfigurableArticle (Marker interface for Articles with context-aware component
    configuration)

Dependencies
------------
    * raptus.article.core

Installation
============

To install raptus.article.gallery into your Plone instance, locate the file
buildout.cfg in the root of your Plone instance directory on the file system,
and open it in a text editor.

Add the actual raptus.article.configuration add-on to the "eggs" section of
buildout.cfg. Look for the section that looks like this::

    eggs =
        Plone

This section might have additional lines if you have other add-ons already
installed. Just add the raptus.article.configuration on a separate line, like this::

    eggs =
        Plone
        raptus.article.configuration

    zcml = 
        raptus.article.configuration

Note that you have to run buildout like this::

    $ bin/buildout

Then go to the "Add-ons" control panel in Plone as an administrator, and
install or reinstall the "raptus.article.configuration" product.

Usage
=====

By default, components store their configuration in ``raptus.article`` property
sheet in portal_properties. With raptus.article.configuration package you can 
override these settings for each instance of Raptus Article. 

For now, the UI for per-context configuration is not polished yet. You have to
use the ZMI to do it. Point your browser to
``http://<path>/<to>/<article>/manage_propertiesForm`` and use
`Add` form to add a new property to your Article. Example:

    * Name: images_galleryright_width
    * Value: 600
    * Type: int

The raptus.article.configuration will then first inspect the entire acquisition
chain of an Article for properties before falling back to getting configuration
from portal_properties.

Copyright and credits
=====================

raptus.article.configuration is copyrighted by `HexagonIT Oy <http://hexagonit.fi>`_ and licensed under the GPL. 
See LICENSE.txt for details.
