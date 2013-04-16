from zope import schema
from five import grok

from Products.CMFCore.utils import getToolByName
from plone.directives import dexterity, form
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.app.textfield import RichText

from collective.gallerypage import MessageFactory as _


class IGalleryPage(form.Schema, IImageScaleTraversable):
    """
    A Gallery Page
    """
    text = RichText(title = _(u'Text'),
        required = False)


class GalleryPage(dexterity.Container):
    grok.implements(IGalleryPage)

    def SearchableText(self):
        value = ''
        if self.text:
            transforms = getToolByName(self, 'portal_transforms')
            stream = transforms.convertTo('text/plain', self.text, mimetype='text/html')
            value = stream.getData().strip()

        print value
        return ' '.join([self.Title(), self.Description(), value,
                         ' '.join([i.encode('utf-8') for i in self.subject])])


class View(grok.View):
    grok.context(IGalleryPage)
    grok.require('zope2.View')
    grok.name('view')

    def get_images(self):
        return self.context.listFolderContents(contentFilter={
            'portal_type': 'Image',
            'sort_on': 'getObjPositionInParent'})

    def get_first_image(self):
        images = self.get_images()
        if not images:
            return None
        return images[0]

    def get_files(self):
        return self.context.listFolderContents(contentFilter={
            'portal_type': 'File',
            'sort_on': 'getObjPositionInParent'})
