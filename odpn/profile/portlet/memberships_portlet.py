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
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets import PloneMessageFactory as _
from plone.memoize import ram
from plone.app.portlets.portlets import base
from Acquisition import aq_inner
from plone.memoize.compress import xhtml_compress
from plone.app.layout.navigation.root import getNavigationRootObject
from odpn.profile import MessageFactory as _


class IContentNavigation(IPortletDataProvider):
    """ Memberships Portlet"""
    pass

class Assignment(base.Assignment):
    implements(IContentNavigation)
    
class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/memberships_portlet.pt')
    
    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def contents(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.searchResults(path= {'query': path, 'depth': 1},
                                        portal_type='odpn.profile.membership')
        memberships = [brain for brain in brains]
        memberships.sort(key=lambda x: x.getObject().membership_year)
        return memberships

class AddForm(base.NullAddForm):
    label = u"Add Memberships Portlet"
    description = ''
    
    def create(self):
        return Assignment()
