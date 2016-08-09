from zope.interface import implements
from zope import schema
from odpn.profile import MessageFactory as _
from plone.supermodel import model
from zope.component import adapter
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.app.users.browser.personalpreferences import UserDataPanel
from plone.z3cform.fieldsets import extensible
from z3c.form.field import Fields
from plone.app.users.browser.register import RegistrationForm
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.directives import dexterity, form
from plone.supermodel import model
from zope import schema
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from plone.app.textfield import RichText
from z3c.form import form
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from plone.z3cform.fieldsets.utils import move
from plone.app.users.browser.formlib import FileUpload
from plone.app.users.browser.interfaces import EmailAddressInvalid
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from zope.interface import invariant, Invalid

def checkEmailAddress(value):
    portal = getUtility(ISiteRoot)

    reg_tool = getToolByName(portal, 'portal_registration')
    if value and reg_tool.isValidEmail(value):
        pass
    else:
        raise EmailAddressInvalid
    return True


class IEnhancedUserDataSchema(IUserDataSchema):
    # ...

    fullname = schema.TextLine(
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

    email = schema.ASCIILine(
        title=_(u'label_email', default=u'Email Address'),
        description=u'',
        required=True,
        constraint=checkEmailAddress)

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

    primary_competencies = schema.TextLine(
        title=_(u'Primary Competencies'),
        required=False,
        )

    secondary_competencies = schema.TextLine(
        title=_(u'Secondary Competencies'),
        required=False,
        )

    user_biography = schema.Text(
        title=_(u'label_user_biography', default=u'Biography'),
        description=_(u'desc_user_biography',
                      default=u"A short overview of who you are and what you do. Will be displayed on your author page, linked from the items you create."),
        required=False,
        )

    portrait = FileUpload(title=_(u'label_portrait', default=u'Portrait'),
        description=_(u'help_portrait',
                      default=u'To add or change the portrait: click the '
                      '"Browse" button; select a picture of yourself. '
                      'Recommended image size is 75 pixels wide by 100 '
                      'pixels tall.'),
        required=False)

    pdelete = schema.Bool(
        title=_(u'label_delete_portrait', default=u'Delete Portrait'),
        description=u'',
        required=False)

    # @invariant
    # def email_validate(data):
    #     if data.email_address_2 !=  data.email:
    #         raise Invalid(_(u"Invalid email address"))

class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEnhancedUserDataSchema
    
    
@adapter(Interface, IDefaultBrowserLayer, UserDataPanel)
class UserDataPanelExtender(extensible.FormExtender):
    
    def update(self):
        fields = Fields(IEnhancedUserDataSchema)
        import pdb; pdb.set_trace()
        self.add(fields)
        
      

class CustomizedUserDataPanel(UserDataPanel):
    def __init__(self, context, request):
        super(CustomizedUserDataPanel, self).__init__(context, request)
        self.form_fields = self.form_fields.omit('description')
        self.form_fields = self.form_fields.omit('location')
        self.form_fields = self.form_fields.omit('home_page')
        self.form_fields['user_biography'].custom_widget = WYSIWYGWidget






