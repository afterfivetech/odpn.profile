from five import grok
from zope.formlib import form
from zope import schema
from zope.interface import implements
from zope.component import getMultiAdapter
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone import api

grok.templatedir('templates')

class IContentNavigation(IPortletDataProvider):
    
    pass


class Assignment(base.Assignment):
    implements(IContentNavigation)
    
    @property
    def title(self):
        return u'Related Resources'
    
class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/odpn_event_resources.pt')
    
    def resources(self):
        context = self.context
        brains = context.portal_catalog.unrestrictedSearchResults(path={'query':'/'.join(context.getPhysicalPath()), 'depth':1}, portal_type='odpn.resources.resource')
        return brains

class AddForm(base.NullAddForm):
    label = u"Add Related Resources Portlet"
    description = ''
    
    def create(self):
        return Assignment()