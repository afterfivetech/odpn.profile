import logging
from zope import event
from DateTime import DateTime
from AccessControl import getSecurityManager
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.events import UserLoggedInEvent
from Products.PlonePAS.events import UserInitialLoginInEvent
from Products.PlonePAS.interfaces import membership
from Products.PlonePAS.utils import cleanId
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import normalizeString

default_portrait = 'defaultUser.png'
logger = logging.getLogger('PlonePAS')
RENAME_AFTER_CREATION_ATTEMPTS = 100
def getMemberareaCreationFlag(self):
    return True

def get_enable_user_folders(self):
    return True

#    security.declarePublic('createMemberarea')
def loginUser(self, REQUEST=None):
        """ Handle a login for the current user.

        This method takes care of all the standard work that needs to be
        done when a user logs in:
        - clear the copy/cut/paste clipboard
        - PAS credentials update
        - sending a logged-in event
        - storing the login time
        - create the member area if it does not exist
        """
        user=getSecurityManager().getUser()
        if user is None:
            return

        res = self.setLoginTimes()
        if res:
            event.notify(UserInitialLoginInEvent(user))
        else:
            event.notify(UserLoggedInEvent(user))

        if REQUEST is None:
            REQUEST=getattr(self, 'REQUEST', None)
        if REQUEST is None:
            return

        # Expire the clipboard
        if REQUEST.get('__cp', None) is not None:
            REQUEST.RESPONSE.expireCookie('__cp', path='/')

        createMemberarea(self)
        try:
            pas = getToolByName(self, 'acl_users')
            pas.credentials_cookie_auth.login()
            #if res:
            #    event.notify(MemberAreaCreatedEvent(user)) 
            #set the cookie __ac so that client can remember it
            myresponse = REQUEST.RESPONSE
            if getattr(REQUEST,"ac_persistent",None):
                cookiename = '__ac'
                cookie = myresponse.cookies.get(cookiename)
                if cookie:
                    cookievalue = cookie.pop('value')
                    new_date = DateTime()+7
                    cookie['expires'] = new_date.strftime("%a, %d-%h-%y %H:%m:%S GMT+8")
                    myresponse.setCookie(cookiename,cookievalue,**cookie)
        except AttributeError:
            # The cookie plugin may not be present
            pass
        try:
            pass
#             event.notify(AddloginlogsEvent(user))
        except AttributeError:
            pass

def isProfileIdAllowed(self, data):
    members = self.getMembersFolder()
    if hasattr(members, data):
        return False
    return True

def createMemberarea(self, member_id=None, minimal=None):
    """
    Create a member area for 'member_id' or the authenticated
    user, but don't assume that member_id is url-safe.
    """
    if not self.getMemberareaCreationFlag():
        return None

    membership = getToolByName(self, 'portal_membership')
    members = self.getMembersFolder()
    if not member_id:
        # member_id is optional (see CMFCore.interfaces.portal_membership:
        #     Create a member area for 'member_id' or authenticated user.)
        member = membership.getAuthenticatedMember()
        member_id = member.getId()

        fname = member.getProperty('first_name', '').split(' ')[0] if member.getProperty('first_name') else ''
        mname = member.getProperty('mid_initial', '')[:1] if member.getProperty('mid_initial') else '' 
        lname = member.getProperty('last_name', '') if member.getProperty('last_name') else ''
        new_id = normalizeString(fname + mname + lname)
        
        if hasattr(members, new_id):
            #context_id = new_id
            return
        else:
            # Try juandcruz-1, juandcruz-2, etc.
            idx = 1
            while idx <= RENAME_AFTER_CREATION_ATTEMPTS:
                if idx == 1:
                    new_id1 = "%s" % new_id
                else:
                    new_id1 = "%s%d" % (new_id, idx-1)
                
                if hasattr(members, new_id1):
                    continue
                else:
                    context_id = new_id1
                    break;
                idx += 1
        
    if hasattr(members, 'aq_explicit'):
        members = members.aq_explicit

    if members is None:
        # no members area
        logger.debug('createMemberarea: members area does not exist.')
        return

    safe_member_id = cleanId(context_id).replace('--', '-')
    if hasattr(members, safe_member_id):
        # has already this member
        logger.debug(
            'createMemberarea: member area '
            'for %r already exists.' % safe_member_id)
        return

    if not safe_member_id:
        # Could be one of two things:
        # - A Emergency User
        # - cleanId made a empty string out of member_id
        logger.debug(
            'createMemberarea: empty member id '
            '(%r, %r), skipping member area creation.' %
            (member_id, safe_member_id)
        )
        return

    # Create member area without security checks
    typesTool = getToolByName(members, 'portal_types')
    fti = typesTool.getTypeInfo(self.memberarea_type)
    member_folder = fti._constructInstance(members, safe_member_id)

    # Get the user object from acl_users
    acl_users = getToolByName(self, "acl_users")
    user = acl_users.getUserById(member_id)
    if user is not None:
        user = user.__of__(acl_users)
    else:
        user = getSecurityManager().getUser()
        # check that we do not do something wrong
        if user.getId() != member_id:
            raise NotImplementedError(
                'cannot get user for member area creation'
            )

    # Modify member folder
    member_folder = self.getHomeFolder(safe_member_id)
    # Grant Ownership and Owner role to Member
    
    member_folder.changeOwnership(user)
    member_folder.__ac_local_roles__ = None
    member_folder.manage_setLocalRoles(member_id, ['Owner'])
    # We use ATCT now use the mutators
    member_folder.setTitle(safe_member_id or member_id)
    member_folder.reindexObject()

    # Hook to allow doing other things after memberarea creation.
    notify_script = getattr(member_folder, 'notifyMemberAreaCreated', None)
    if notify_script is not None:
        notify_script()

