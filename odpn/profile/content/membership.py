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


# Interface class; used to define content-type schema.

class IMembership(form.Schema, IImageScaleTraversable):
    """
    Membership
    """

    membership_year = schema.TextLine(
        title=_(u'Year'),
        required=True
    )

    membership_type = schema.TextLine(
        title=_(u'Type'),
        required=True
    )

    category = schema.TextLine(
        title=_(u'Category'),
        required=True
    )

    receipt_no = schema.TextLine(
        title=_(u'Receipt No'),
        required=True
    )

    membership_validity = schema.Date(
        title=_(u'Year'),
        required=True
    )



    pass

alsoProvides(IMembership, IFormFieldProvider)
