from Products.CMFCore.utils import getToolByName
from plone.app.users.browser.register import RegistrationForm as Original_RegistrationForm
from plone.app.users.browser.register import AddUserForm as Original_AddUserForm
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import normalizeString

# Number of retries for creating a user id like bobjjones-42:
RENAME_AFTER_CREATION_ATTEMPTS = 100

def generate_user_id(self, data):
    """Generate a user id from data.
    """
    fname = data.get('first_name', '').split(' ')[0] if data.get('first_name') else ''
    mname = data.get('mid_initial', '') if data.get('mid_initial') else ''
    lname = data.get('last_name', '') if data.get('last_name') else ''
    new_id = normalizeString(fname + mname + lname)

    registration = getToolByName(self.context, 'portal_registration')
    if hasattr(registration, '_ALLOWED_MEMBER_ID_PATTERN'):
        if not registration._ALLOWED_MEMBER_ID_PATTERN.match(new_id):
            # If 'bobjjones' is not good then 'bobjjones-1' will not
            # be good either.
            data['username'] = new_id
            data['user_id'] = new_id
            return new_id
    if registration.isMemberIdAllowed(new_id):
        data['username'] = new_id
        data['user_id'] = new_id
        return new_id
    # Try bobjjones-1, bobjjones-2, etc.
    idx = 1
    while idx <= RENAME_AFTER_CREATION_ATTEMPTS:
        new_id1 = "%s-%d" % (new_id, idx)
        if registration.isMemberIdAllowed(new_id1):
            data['username'] = new_id1
            data['user_id'] = new_id1
            return new_id1
        idx += 1

class AddUserForm(Original_AddUserForm):
    generate_user_id = generate_user_id

class RegistrationForm(Original_RegistrationForm):
    generate_user_id = generate_user_id
