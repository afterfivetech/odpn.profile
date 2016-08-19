from five import grok
from plone.directives import dexterity, form
from Products.CMFCore.utils import getToolByName
from plone import api
from odpn.profile.content.odpn_event import IODPNEvent

grok.templatedir('templates')

class manage_attendance(dexterity.DisplayForm):
    grok.context(IODPNEvent)
    grok.require('zope2.View')
    