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


# Interface class; used to define content-type schema.

class IResource(form.Schema, IImageScaleTraversable):
    """
    Resource
    """
    authors = schema.Text(
           title=_(u"Authors"),
           required=True,
        )
    resource_type = schema.TextLine(
           title=_(u"Type"),
           required=True,
        )
    pass

alsoProvides(IResource, IFormFieldProvider)
