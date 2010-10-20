from zope import interface

class ITeaser(interface.Interface):
    """ Handler for teaser thumbing and captioning
    """
        
    def getTeaserURL(size="original"):
        """
        Returns the url to the teaser image in the specific size
        
        The sizes are taken from the raptus_article properties sheet
        and are formed by the following name schema:
        
            teaser_<size>_(height|width)
        """
    
    def getTeaser(size="orginal"):
        """ 
        Returns the html tag of the teaser image in the specific size
        
        The sizes are taken from the raptus_article properties sheet
        and are formed by the following name schema:
        
            teaser_<size>_(height|width)
        """
        
    def getSize(size):
        """
        Returns the width and height registered for the specific size
        """
    
    def getCaption():
        """
        Returns the caption for the image
        """