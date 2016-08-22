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

from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.component import getMultiAdapter, getUtility
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.constants import USER_CATEGORY
from plone.portlets.constants import GROUP_CATEGORY
from plone.portlets.constants import CONTENT_TYPE_CATEGORY
from plone.portlets.constants import CONTEXT_CATEGORY


# Interface class; used to define content-type schema.

class IProfile(form.Schema, IImageScaleTraversable):
    """
    Profile
    """
    pass

alsoProvides(IProfile, IFormFieldProvider)

@grok.subscribe(IProfile, IObjectAddedEvent)
def _createObject(context, event):
    for manager_name in ('plone.leftcolumn','plone.rightcolumn'):
        manager = getUtility(IPortletManager, name=manager_name)
        assignable = getMultiAdapter((context, manager,), ILocalPortletAssignmentManager)
        for category in (GROUP_CATEGORY,CONTEXT_CATEGORY,USER_CATEGORY):
            assignable.setBlacklistStatus(category, 1)
