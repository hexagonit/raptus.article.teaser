from zope.interface import implements
from zope.component import adapts

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField

try: # blob
    from plone.app.blob.field import ImageField
except:
    from Products.Archetypes.Field import ImageField

from Products.validation import V_REQUIRED
from Products.Archetypes import atapi
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes import ATCTMessageFactory as _at

from raptus.article.core import RaptusArticleMessageFactory as _
from raptus.article.core.interfaces import IArticle

class ImageField(ExtensionField, ImageField):
    """ ImageField
    """

class StringField(ExtensionField, atapi.StringField):
    """ StringField
    """
    
class ArticleExtender(object):
    """ Adds the image and caption fields to the article schema
    """
    implements(ISchemaExtender)
    adapts(IArticle)

    fields = [
        ImageField('image',
            required=False,
            languageIndependent=True,
            storage = atapi.AnnotationStorage(),
            swallowResizeExceptions = zconf.swallowImageResizeExceptions.enable,
            pil_quality = zconf.pil_config.quality,
            pil_resize_algo = zconf.pil_config.resize_algo,
            max_size = zconf.ATImage.max_image_dimension,
            sizes= {'large'   : (768, 768),
                    'preview' : (400, 400),
                    'mini'    : (200, 200),
                    'thumb'   : (128, 128),
                    'tile'    :  (64, 64),
                    'icon'    :  (32, 32),
                    'listing' :  (16, 16),
                   },
            validators = (('isNonEmptyFile', V_REQUIRED),
                          ('checkImageMaxSize', V_REQUIRED)),
            widget = atapi.ImageWidget(
                description = '',
                label= _at(u'label_image', default=u'Image'),
                show_content_type = False,
            )
        ),
        
        StringField('imageCaption',
            required = False,
            searchable = True,
            widget = atapi.StringWidget(
                description = '',
                label = _at(u'label_image_caption', default=u'Image Caption'),
                size = 40
            )
        ),
    ]

    def __init__(self, context):
         self.context = context
         
    def getFields(self):
        return self.fields
