from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
#from plone.multilingualbehavior.directives import languageindependent
from collective import dexteritytextindexer

from odpn.profile import MessageFactory as _
from plone import api
from plone.app.users.schema import checkEmailAddress
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectModifiedEvent
from zope.container.interfaces import INameChooser
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

class IRegistration(form.Schema, IImageScaleTraversable):
    """
    Registration
    """
    first_name = schema.TextLine(
        title=_(u'First Name'),
        required=True
    )

    mid_initial = schema.TextLine(
        title=_(u'Middle Initial'),
        required=True
    )

    last_name = schema.TextLine(
        title=_(u'Last Name'),
        required=True
    )

    email_address = schema.TextLine(
        title=_(u'Email Address'),
        required=True,
        constraint=checkEmailAddress,
    )

    cellphone_no = schema.TextLine(
        title=_(u'Cellphone No.'),
        required=True
    )
    
    form.mode(title='hidden')
    title = schema.TextLine(
        title = u"Title",
        required = False
    )

alsoProvides(IRegistration, IFormFieldProvider)

def getUser():
    if not api.user.is_anonymous():
        current = api.user.get_current()
        if hasattr(current, 'getProperty'):
            return current
    return ''

@form.default_value(field=IRegistration['first_name'])
def getData(self):
    if getUser():
        return getUser().getProperty("first_name")
    return ''

@form.default_value(field=IRegistration['mid_initial'])
def getData(self):
    if getUser():
        return getUser().getProperty("mid_initial")
    return ''

@form.default_value(field=IRegistration['last_name'])
def getData(self):
    if getUser():
        return getUser().getProperty("last_name")
    return ''

@form.default_value(field=IRegistration['email_address'])
def getData(self):
    if getUser():
        return getUser().getProperty("email")
    return ''

@form.default_value(field=IRegistration['cellphone_no'])
def getData(self):
    if getUser():
        return getUser().getProperty("cellphone_no")
    return ''


@grok.subscribe(IRegistration, IObjectAddedEvent)
def _createObj(context, event):
    title = '%s %s %s' % (context.first_name, context.mid_initial[0] or '', context.last_name)
    parent = context.aq_parent
    #context.setTitle(title)
    context.title = title
    oid = INameChooser(parent).chooseName(title, context)
    #setattr(context, 'id', oid)
    context.reindexObject()
    statusmsg = IStatusMessage(context.REQUEST)
    #statusmsg.add("Thank you for registering to this event.  We will confirm your registration by email", type=u"success")
    context.plone_utils.addPortalMessage("Thank you for registering to this event.  We will confirm your registration by email.", "success")
    return


@grok.subscribe(IRegistration, IObjectModifiedEvent)
def _modifyObj(context, event):
    title = context.title
    parent = context.aq_parent.aq_inner
    oid = INameChooser(parent).chooseName(title, context)
    if context.cb_userHasCopyOrMovePermission() and context.cb_isMoveable():
        parent.manage_renameObject(context.getId(), oid)
    
    context.reindexObject()
    return

class IRegistrationAddForm(dexterity.AddForm):
    grok.name('odpn.profile.registration')
    template = ViewPageTemplateFile('templates/registrationaddform.pt')
    form.wrap(False)
    

class IRegistrationEditForm(dexterity.EditForm):
    grok.context(IRegistration)
    template = ViewPageTemplateFile('templates/registrationeditform.pt')

