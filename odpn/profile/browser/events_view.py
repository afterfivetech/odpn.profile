from five import grok
from plone.directives import dexterity, form
from odpn.profile.content.events import IEvents

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IEvents)
    grok.require('zope2.View')
    grok.template('events_view')
    grok.name('view')

