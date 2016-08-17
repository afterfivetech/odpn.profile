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

# Interface class; used to define content-type schema.

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
        required=True
    )

    cellphone_no = schema.TextLine(
        title=_(u'Cellphone No.'),
        required=True
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
    return getUser().getProperty("first_name")

@form.default_value(field=IRegistration['mid_initial'])
def getData(self):
    return getUser().getProperty("mid_initial")

@form.default_value(field=IRegistration['last_name'])
def getData(self):
    return getUser().getProperty("last_name")

@form.default_value(field=IRegistration['email_address'])
def getData(self):
    return getUser().getProperty("email")

@form.default_value(field=IRegistration['cellphone_no'])
def getData(self):
    return getUser().getProperty("cellphone_no")




