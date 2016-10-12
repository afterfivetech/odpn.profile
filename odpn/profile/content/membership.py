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
from collective import dexteritytextindexer

from odpn.profile import MessageFactory as _
from datetime import date
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectModifiedEvent
from zope.container.interfaces import INameChooser
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

membershiptype=SimpleVocabulary(
    [SimpleTerm(value=u'Application',title=_(u'Application')),
    SimpleTerm(value=u'Renewal',title=_(u'Renewal'))]
)


# Interface class; used to define content-type schema.

class IMembership(form.Schema, IImageScaleTraversable):
    """
    Membership
    """

    membership_year = schema.TextLine(
        title=_(u'Membership Year'),
        required=True
    )

    membership_type = schema.Choice(
        title=_(u'Type'),
        vocabulary=membershiptype,
        required=False
    )

    category = schema.TextLine(
        title=_(u'Category'),
        required=False
    )

    receipt_no = schema.TextLine(
        title=_(u'Receipt No'),
        required=False
    )

    membership_validity = schema.Date(
        title=_(u'Membership Validity'),
        required=False
    )
    
    form.mode(title='hidden')
    title =  schema.TextLine(
        title=u"Title",
        required=False
    )



    pass

alsoProvides(IMembership, IFormFieldProvider)

@form.default_value(field=IMembership['membership_year'])
def getData(self):
    return date.today().year

@form.default_value(field=IMembership['membership_validity'])
def getData(self):
    return date.today().replace(date.today().year+1)


@grok.subscribe(IMembership, IObjectAddedEvent)
def _createObj(context, event):
    #title = '%s-%s' % (context.membership_year, context.membership_type)
    #parent = context.aq_parent
    #context.setTitle(title)
    #context.title = title
    #oid = INameChooser(parent).chooseName(title, context)
    #setattr(context, 'id', oid)
    #context.reindexObject()
    
    return

@grok.subscribe(IMembership, IObjectModifiedEvent)
def _modifyObj(context, event):
    title = context.title
    parent = context.aq_parent.aq_inner
    oid = INameChooser(parent).chooseName(title, context)
    if context.cb_userHasCopyOrMovePermission() and context.cb_isMoveable():
        parent.manage_renameObject(context.getId(), oid)
    
    context.reindexObject()
    return


class IMembershipAddForm(dexterity.AddForm):
    grok.name('odpn.profile.membership')
    template = ViewPageTemplateFile('templates/membershipaddform.pt')
    form.wrap(False)
    

class IMembershipEditForm(dexterity.EditForm):
    grok.context(IMembership)
    template = ViewPageTemplateFile('templates/membershipeditform.pt')