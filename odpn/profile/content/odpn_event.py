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
from plone.app.contenttypes.content import Event
from zope.lifecycleevent.interfaces import IObjectAddedEvent

# Interface class; used to define content-type schema.

# class IODPNEvent(Event):
# 	"""Convenience subclass for ``Event`` portal type"""


class IODPNEvent(form.Schema):
    """
       Marker/Form interface for ODPN Resource
    """
    # -*- Your Zope schema definitions here ... -*-

alsoProvides(IODPNEvent,IFormFieldProvider)

@grok.subscribe(IODPNEvent, IObjectAddedEvent)
def _createObj(context, event):
    context.setLayout("event_view")
    return
