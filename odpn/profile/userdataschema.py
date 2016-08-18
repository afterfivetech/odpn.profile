from plone.app.users.browser.account import AccountPanelSchemaAdapter
from plone.app.users.browser.account import AccountPanelForm

from zope.interface import implements
from zope import schema
from odpn.profile import MessageFactory as _
from plone.supermodel import model
from zope.component import adapter
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.z3cform.fieldsets import extensible
from z3c.form.field import Fields
from plone.app.users.browser.register import RegistrationForm
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.directives import dexterity, form
from plone.supermodel import model
from zope import schema
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from plone.app.textfield import RichText
from z3c.form import form
from plone.z3cform.fieldsets.utils import move
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from zope.interface import invariant, Invalid
from plone.app.users.browser.userdatapanel import UserDataPanel
from plone.autoform import directives
from z3c.form.interfaces import HIDDEN_MODE, INPUT_MODE, DISPLAY_MODE, HIDDEN_MODE
from odpn.profile.interfaces import IProductSpecific
from plone.app.users.browser.register import RegistrationForm, AddUserForm
from five import grok
from zope.schema.interfaces import IContextSourceBinder
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from odpn.profile.interfaces import ICompetencyDGForm
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


@grok.provider(IContextSourceBinder)
def competency_val(context):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ICompetencyDGForm, check=False)
    values = []
    if settings.competencies:
        for val in settings.competencies:
            values.append(SimpleTerm(value=val['primary_competencies_values'], token=val['primary_competencies_values'], title=val['primary_competencies_values']))
    return SimpleVocabulary(values)

class IEnhancedUserDataSchema(model.Schema):

    # fullname = schema.TextLine(
    #     title=_(u'First Name'),
    #     required=False,
    #     )
    first_name = schema.TextLine(
        title=_(u'First Name'),
        required=False,
        )

    mid_initial = schema.TextLine(
        title=_(u'Middle Initial'),
        required=False,
        )

    last_name = schema.TextLine(
        title=_(u'Last Name'),
        required=False,
        )

    telephone_no = schema.TextLine(
        title=_(u'Telephone No.'),
        required=False,
        )

    cellphone_no = schema.TextLine(
        title=_(u'Cellphone No.'),
        required=False,
        )

    # email = schema.ASCIILine(
    #     title=_(u'label_email', default=u'Email Address'),
    #     description=u'',
    #     required=True,
    #     constraint=checkEmailAddress)

    # email_address_2 = schema.TextLine(
    #     title=_(u'Email Address'),
    #     description=_(u'email_address_2',
    #                   default=u"Reenter E-mail"),
    #     required=True,
    #     )

    industry = schema.TextLine(
        title=_(u'Industry'),
        required=False,
        )

    primary_competencies = schema.Choice(
        title=_(u'Primary Competencies'),
        source = competency_val,
        required=False,
        )

    secondary_competencies = schema.Choice(
        title=_(u'Secondary Competencies'),
        source = competency_val,
        required=False,
        )

    # user_biography = schema.Text(
    #     title=_(u'label_user_biography', default=u'Biography'),
    #     description=_(u'desc_user_biography',
    #                   default=u"A short overview of who you are and what you do. Will be displayed on your author page, linked from the items you create."),
    #     required=False,
    #     )

    # portrait = FileUpload(title=_(u'label_portrait', default=u'Portrait'),
    #     description=_(u'help_portrait',
    #                   default=u'To add or change the portrait: click the '
    #                   '"Browse" button; select a picture of yourself. '
    #                   'Recommended image size is 75 pixels wide by 100 '
    #                   'pixels tall.'),
    #     required=False)

    # pdelete = schema.Bool(
    #     title=_(u'label_delete_portrait', default=u'Delete Portrait'),
    #     description=u'',
    #     required=False)
    

@adapter(Interface, IProductSpecific, UserDataPanel)
class UserDataPanelExtender(extensible.FormExtender):
    def update(self):
        fields = Fields(IEnhancedUserDataSchema)
        if 'fullname' in self.form.fields.keys():
            #self.remove('fullname')
            self.form.fields['fullname'].mode = HIDDEN_MODE
        self.add(fields)
        #self.remove('portrait')
        self.move('email', after='cellphone_no')
        self.move('description', after='secondary_competencies')
        if 'portrait' in self.form.fields.keys():
            self.move('portrait', after='description')
        if 'location' in self.form.fields.keys():
            self.move('location', after='description')
        if 'home_page' in self.form.fields.keys():
            self.move('home_page', after='description')
        #self.form.fields['fullname'].mode = HIDDEN_MODE
        
        

    
@adapter(Interface, IProductSpecific, AddUserForm)
class AddUserFormExtender(extensible.FormExtender):
    

    def update(self):
        fields = Fields(IEnhancedUserDataSchema)
        if 'fullname' in self.form.fields.keys():
            self.form.fields['fullname'].mode = HIDDEN_MODE
        self.add(fields)
        self.move('email', after='cellphone_no')
        self.move('mail_me', after='last_name')
        self.move('password_ctl', after='last_name')
        self.move('password', after='last_name')
        self.move('username', after='last_name')
        
        
        
            
        
@adapter(Interface, IProductSpecific, RegistrationForm)
class RegistrationPanelExtender(extensible.FormExtender):
    
    def update(self):
        fields = Fields(IEnhancedUserDataSchema)
        if 'fullname' in self.form.fields.keys():
            self.form.fields['fullname'].mode = HIDDEN_MODE
        self.add(fields)
        self.move('email', after='cellphone_no')
        self.move('mail_me', after='last_name')
        self.move('password_ctl', after='last_name')
        self.move('password', after='last_name')
        self.move('username', after='last_name')
        
        
            
class EnhancedUserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IEnhancedUserDataSchema
    

