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

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import normalizeString
from plone import api


# Interface class; used to define content-type schema.

class IProfile(form.Schema, IImageScaleTraversable):
    """
    Profile
    """
    pass

alsoProvides(IProfile, IFormFieldProvider)

# Number of retries for creating a user id like juandcruz-55:
RENAME_AFTER_CREATION_ATTEMPTS = 100

def isProfileIdAllowed(context, data):
	catalog = getToolByName(context, 'portal_catalog')
	path = '/'.join(context.aq_parent.getPhysicalPath())
	brains = catalog.unrestrictedSearchResults(path={'query': path,'depth':1},
												portal_type='odpn.profile.profile')

	return True if data not in [brain.getId for brain in brains] else False

@grok.subscribe(IProfile, IObjectAddedEvent)
def _createObject(context, event):
    """Generate a user id from data.
    """
    for manager_name in ('plone.leftcolumn','plone.rightcolumn'):
        manager = getUtility(IPortletManager, name=manager_name)
        assignable = getMultiAdapter((context, manager,), ILocalPortletAssignmentManager)
        for category in (GROUP_CATEGORY,CONTEXT_CATEGORY,USER_CATEGORY):
            assignable.setBlacklistStatus(category, 1)

    parent = context.aq_parent
    membership = getToolByName(context, 'portal_membership')
    user = api.user.get(username= context.owner_info()['id'])

    fname = user.getProperty('first_name', '').split(' ')[0] if user.getProperty('first_name') else ''
    mname = user.getProperty('mid_initial', '')[:1] if user.getProperty('mid_initial') else '' 
    lname = user.getProperty('last_name', '') if user.getProperty('last_name') else ''
    new_id = normalizeString(fname + mname + lname)
    if isProfileIdAllowed(context, new_id):
    	context_id = new_id
    else:
    	# Try juandcruz-1, juandcruz-2, etc.
    	idx = 1
    	while idx <= RENAME_AFTER_CREATION_ATTEMPTS:
	        new_id1 = "%s-%d" % (new_id, idx)
	        if isProfileIdAllowed(context, new_id1):
	            context_id = new_id1
	            break;
	        idx += 1
    if context_id:
	    parent.manage_renameObject(context.getId(), context_id) 
	    context.reindexObject()
    return

