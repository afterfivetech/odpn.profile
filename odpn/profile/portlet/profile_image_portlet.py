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
    """ Profile Image Portlet"""
    pass


class Assignment(base.Assignment):
    implements(IContentNavigation)
    
    @property
    def title(self):
        return _('Profile Image Portlet')
    

class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/profile_image_portlet.pt')
    
    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        
    def contents(self):
        
        membership = getToolByName(self.context, 'portal_membership')
        user_id = self.context.owner_info()['id']
        user = membership.getMemberById(user_id)
        
        info = {'portrait':'#',
                'fullname':'',
                'industry':'',
                'contact_details':'',
                'primary_competencies':'',
                'secondary_competencies':'',
                'biography':''}
        if user:
            
            if self.context.portal_membership.getPersonalPortrait(user_id):
                info['portrait'] = self.context.portal_membership.getPersonalPortrait(user_id).absolute_url()
            else:
                if user.getPersonalPortrait():
                    info['portrait'] = user.getPersonalPortrait().absolute_url()
            info['fullname'] = user.getProperty('first_name')+' '+user.getProperty('mid_initial')+'. '+user.getProperty('last_name')
            info['industry'] = user.getProperty('industry')
            info['primary_competencies'] = user.getProperty('primary_competencies')
            info['secondary_competencies'] = user.getProperty('secondary_competencies')
            info['biography'] = user.getProperty('description')
            if user.getProperty('telephone_no'):
                info['contact_details'] = 'Tel. No. '+user.getProperty('telephone_no')+' '
            if user.getProperty('cellphone_no'):
                info['contact_details'] += 'Cell. No. '+user.getProperty('cellphone_no')
        return info
    
    def filter_edit_profile(self):
        current_user = self.context.portal_membership.getAuthenticatedMember().getUserName()
        if self.context.owner_info()['id'] == current_user:
                return True
        return False


class AddForm(base.NullAddForm):
    label = u"Add Profile Image Portlet"
    description = ''
    
    def create(self):
        return Assignment()
    
