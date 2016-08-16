from five import grok
from plone.directives import dexterity, form
from odpn.profile.content.profile import IProfile
from plone import api
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IProfile)
    grok.require('zope2.View')
    grok.template('profile_view')
    grok.name('view')
    
    def user_info(self):
        user_id = self.context.id
        membership = getToolByName(self.context, 'portal_membership')
        user = membership.getMemberById(user_id)
        info = {'portrait':'#',
                'fullname':'',
                'industry':'',
                'contact_details':'',
                'primary_competencies':'',
                'secondary_competencies':'',
                'biography':''}
        if user:
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

