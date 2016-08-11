from five import grok
from plone.directives import dexterity, form
from odpn.profile.content.odpn_event import IODPNEvent

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IODPNEvent)
    grok.require('zope2.View')
    grok.template('odpn_event_view')
    grok.name('view')

