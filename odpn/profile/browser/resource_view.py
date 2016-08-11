from five import grok
from plone.directives import dexterity, form
from odpn.profile.content.resource import IResource

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IResource)
    grok.require('zope2.View')
    grok.template('resource_view')
    grok.name('view')

