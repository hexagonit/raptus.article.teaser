from zope import interface, component

from Products.CMFCore.utils import getToolByName

from raptus.article.core.interfaces import IArticle
from raptus.article.teaser.interfaces import ITeaser

class Teaser(object):
    """ Handler for teaser thumbing and captioning
    """
    interface.implements(ITeaser)
    component.adapts(IArticle)
    
    def __init__(self, context):
        self.context = context
        
    def getTeaserURL(self, size="original"):
        """
        Returns the url to the teaser image in the specific size
        
        The sizes are taken from the raptus_article properties sheet
        and are formed by the following name schema:
        
            teaser_<size>_(height|width)
        """
        if not self.context.Schema()['image'].get(self.context):
            return None
        
        w, h = self.getSize(size)
        
        url = '%s/image' % self.context.absolute_url()
        if w or h:
            scales = component.getMultiAdapter((self.context, self.context.REQUEST), name='images')
            scale = scales.scale('image', width=(w or 100000), height=(h or 100000))
            if scale is not None:
                url = scale.url
        return url
        
    def getTeaser(self, size="original"):
        """ 
        Returns the html tag of the teaser image in the specific size
        
        The sizes are taken from the raptus_article properties sheet
        and are formed by the following name schema:
        
            teaser_<size>_(height|width)
        """
        url = self.getTeaserURL(size)
        if not url:
            return None
        
        return '<img src="%s" alt="%s" />' % (url, self.getCaption())
        
    def getSize(self, size):
        """
        Returns the width and height registered for the specific size
        """
        props = getToolByName(self.context, 'portal_properties').raptus_article
        return props.getProperty('teaser_%s_width' % size, 0), props.getProperty('teaser_%s_height' % size, 0)
    
    def getCaption(self, non_default = False):
        """
        Returns the caption for the image.
        If the flag non_default is set it's return a empty string if the caption are empty too
        """
        if (non_default):
            return self.context.Schema()['imageCaption'].get(self.context)
        else:
            return self.context.Schema()['imageCaption'].get(self.context) or self.context.Title()
