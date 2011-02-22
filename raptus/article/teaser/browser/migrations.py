import os
from Acquisition import aq_inner
from zope.annotation.interfaces import IAnnotations

from plone.app.blob.migrations import haveContentMigrations
from plone.app.blob.browser.migration import ImageMigrationView
from plone.app.blob.browser.migration import __file__ as location
from plone.app.blob.migrations import ATImageToBlobImageMigrator
from plone.app.blob.migrations import migrate
from plone.app.blob.migrations import getMigrationWalker

from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _


class ArticleTeaserToBlobImageMigrator(ATImageToBlobImageMigrator):
    
    src_portal_type = 'Article'
    src_meta_type = 'Article'
    dst_portal_type = 'Article'
    dst_meta_type = 'Article'

    def migrate_data(self):
        annotations = IAnnotations(self.old)
        img = annotations.get('Archetypes.storage.AnnotationStorage-image', None)
        if img:
            self.new.Schema()['image'].set(self.new, img)
            del annotations['Archetypes.storage.AnnotationStorage-image']

    def createNew(self):
        self.new = self.old
        
    def remove(self):
        pass

    def reorder(self):
        pass
    
    def renameOld(self):
        pass

class ArticleTeaserMigrationView(ImageMigrationView):
    
    index = ViewPageTemplateFile('%s/migration.pt' % os.path.dirname(location))
    
    def __call__(self):
        context = aq_inner(self.context)
        request = aq_inner(self.request)
        walker = self.walker()
        options = dict(target_type=walker.src_portal_type)
        clicked = request.form.has_key
        portal_url = getToolByName(context, 'portal_url')()
        if not haveContentMigrations:
            msg = _(u'Please install contentmigrations to be able to migrate to blobs.')
            IStatusMessage(request).addStatusMessage(msg, type='warning')
            options['nomigrations'] = 42
        elif clicked('migrate'):
            output = self.migration()
            # Only count actual migration lines
            lines = output.split('\n')
            count = len([l for l in lines if l.startswith('Migrating')])
            msg = _(u'blob_migration_info',
                default=u'Blob migration performed for ${count} item(s).',
                mapping={'count': count})
            IStatusMessage(request).addStatusMessage(msg, type='info')
            options['count'] = count
            options['output'] = output
        elif clicked('cancel'):
            msg = _(u'Blob migration cancelled.')
            IStatusMessage(request).addStatusMessage(msg, type='info')
            request.RESPONSE.redirect(portal_url)
        else:
            options['available'] = len(list(walker.walk()))
        return self.index(**options)
    
    def migration(self):
        return migrate(self, walker=ArticleTeaserMigrationView.walker)
    
    def walker(self):
        return getMigrationWalker(self, migrator=ArticleTeaserToBlobImageMigrator)