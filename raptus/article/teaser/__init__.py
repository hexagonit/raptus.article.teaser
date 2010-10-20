# 

from Products.ATContentTypes.content.image import ATImage
from Products.Archetypes.fieldproperty import ATFieldProperty

from raptus.article.core.content import article

def _tag(self, **kwargs):
    """Generate image tag using the api of the ImageField
    """
    return self.getField('image').tag(self, **kwargs)

def __bobo_traverse__(self, REQUEST, name):
    """Transparent access to image scales
    """
    if name.startswith('image'):
        field = self.getField('image')
        image = None
        if name == 'image':
            image = field.getScale(self)
        else:
            scalename = name[len('image_'):]
            if scalename in field.getAvailableSizes(self):
                image = field.getScale(self, scale=scalename)
        if image is not None and not isinstance(image, basestring):
            # image might be None or '' for empty images
            return image

    return super(article.Article, self).__bobo_traverse__(REQUEST, name)

article.Article.tag = _tag
article.Article.__bobo_traverse__ = __bobo_traverse__
article.Article.image = ATFieldProperty('image')