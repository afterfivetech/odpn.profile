from five import grok
from plone.directives import dexterity, form
from odpn.profile.content.profile import IProfile

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IProfile)
    grok.require('zope2.View')
    grok.template('profile_view')
    grok.name('view')

