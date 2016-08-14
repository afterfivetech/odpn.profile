from Products.CMFPlone.controlpanel.browser.usergroups_usersoverview import UsersOverviewControlPanel

class UserOverviewControlPanel(UsersOverviewControlPanel):
    
    def member_name(self, userid=None):
        context = self.context
        portal_membership = context.portal_membership
        result = ''
        if userid:
            member = portal_membership.getMemberById(userid)
            if member.getProperty('first_name'):
                result += member.getProperty('first_name')
            if member.getProperty('last_name'):
                result += ' '+member.getProperty('last_name')
        return result