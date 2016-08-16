from five import grok
from plone.directives import dexterity, form
from odpn.profile.content.membership import IMembership

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IMembership)
    grok.require('zope2.View')
    grok.template('membership_view')
    grok.name('view')

