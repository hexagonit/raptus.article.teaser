Introduction
============

raptus.article.teaser provides support for adding a teaser image on article.

The following features for raptus.article are provided by this package:

Fields
------
    * Provides an image field for the articles.

Components
----------
    * raptus.article.teaser.full
    * raptus.article.teaser.right
    * raptus.article.teaser.left

Dependencies
------------
    * collective.flowplayer
    * Products.ContentTypeValidator
    * raptus.article.core
    * plone.app.imaging

Installation
============

To install raptus.article.teaser into your Plone instance, locate the file
buildout.cfg in the root of your Plone instance directory on the file system,
and open it in a text editor.

Add the actual raptus.article.teaser add-on to the "eggs" section of
buildout.cfg. Look for the section that looks like this::

    eggs =
        Plone

This section might have additional lines if you have other add-ons already
installed. Just add the raptus.article.teaser on a separate line, like this::

    eggs =
        Plone
        raptus.article.teaser

Note that you have to run buildout like this::

    $ bin/buildout

Then go to the "Add-ons" control panel in Plone as an administrator, and
install or reinstall the "raptus.article.default" product.

Note that if you do not use the raptus.article.default package you have to
include the zcml of raptus.article.teaser either by adding it
to the zcml list in your buildout or by including it in another package's
configure.zcml.

Plone 3 compatibility
---------------------

This packages requires plone.app.imaging which requires two pins in buildout
when using Plone 3, which there are::

    Products.Archetypes = 1.5.16
    plone.scale = 1.2

Migration
=========

Blob-storage
------------

call this view on myplone/@@blob-article-teaser-migration and run the migration.
all media have a separate view at myplone/@@blob-article-media-migration.

Usage
=====

Components
----------
Navigate to the "Components" tab of your article and select one of the teaser image
components and press "save and view". Note that at the article requires an image to
be set in the edit form for the components to display.

Copyright and credits
=====================

raptus.article is copyrighted by `Raptus AG <http://raptus.com>`_ and licensed under the GPL. 
See LICENSE.txt for details.
