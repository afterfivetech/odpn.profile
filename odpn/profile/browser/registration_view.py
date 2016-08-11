from five import grok
from plone.directives import dexterity, form
from odpn.profile.content.registration import IRegistration

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IRegistration)
    grok.require('zope2.View')
    grok.template('registration_view')
    grok.name('view')

