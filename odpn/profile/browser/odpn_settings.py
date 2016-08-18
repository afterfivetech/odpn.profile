from five import grok
from Products.CMFCore.interfaces import ISiteRoot

grok.templatedir('templates')

class odpn_settings(grok.View):
    grok.name('odpn-settings')
    grok.context(ISiteRoot)