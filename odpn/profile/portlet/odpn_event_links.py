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
    
    add_resources = schema.TextLine(
            title = u"'Add Resource' Button Label",
            required=False,
            default = u"Add Resource",
        )

    register = schema.TextLine(
            title = u"Register Button Label",
            required=False,
            default = u"Register",
        )

    manage_registrations = schema.TextLine(
            title = u"Manage Registrations Button Label",
            required=False,
            default = u"Manage Registrations",
        )


class Assignment(base.Assignment):
    implements(IContentNavigation)
    
    
    def __init__(self, button_description=None):
        self.button_description = button_description
       
       
    @property
    def title(self):
        return "Add Register Portlet"
    

class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/odpn_event_links.pt')
    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.data = data
        
        
    def contents(self):
        return self.data

    def isAdmin(self):
        current = str(api.user.get_current())
        roles = ''
        if current != 'Anonymous User':
            roles = api.user.get_roles(username=current, obj= self.context)
        allowed =  ['Administrator', 'Manager'] 
  
        return any((True for x in roles if x in allowed))

    def isMember(self):
        current = str(api.user.get_current())
        roles = ''
        if current != 'Anonymous User':
            roles = api.user.get_roles(username=current, obj= self.context)
        allowed =  ['Authenticated'] 
  
        return any((True for x in roles if x in allowed))

class AddForm(base.AddForm):
    form_fields = form.Fields(IContentNavigation)
    label = u"Add 'Add ODPN Links Portlet'"
    description = ''
    
    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IContentNavigation)
    label = u"Edit 'ODPN Links Portlet'"
    description = ''
