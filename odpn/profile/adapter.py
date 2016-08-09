from plone.app.users.browser.account import AccountPanelSchemaAdapter
from odpn.profile.userdataschema import IEnhancedUserDataSchema
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter

class EnhancedUserDataSchemaAdapter(UserDataPanelAdapter):
    #schema = IEnhancedUserDataSchema
    
    def get_mid_initial(self):
        return self.context.getProperty('mid_initial', '')
    def set_mid_initial(self, value):
        return self.context.setMemberProperties({'mid_initial': value})
    mid_initial = property(get_mid_initial, set_mid_initial)

    def get_last_name(self):
        return self.context.getProperty('last_name', '')
    def set_last_name(self, value):
        return self.context.setMemberProperties({'last_name': value})
    last_name = property(get_last_name, set_last_name)

    def get_telephone_no(self):
        return self.context.getProperty('telephone_no', '')
    def set_telephone_no(self, value):
        return self.context.setMemberProperties({'telephone_no': value})
    telephone_no = property(get_telephone_no, set_telephone_no)

    def get_cellphone_no(self):
        return self.context.getProperty('cellphone_no', '')
    def set_cellphone_no(self, value):
        return self.context.setMemberProperties({'cellphone_no': value})
    cellphone_no = property(get_cellphone_no, set_cellphone_no)

    def get_email_address_2(self):
        return self.context.getProperty('email_address_2', '')
    def set_email_address_2(self, value):
        return self.context.setMemberProperties({'email_address_2': value})
    email_address_2 = property(get_email_address_2, set_email_address_2)

    def get_industry(self):
        return self.context.getProperty('industry', '')
    def set_industry(self, value):
        return self.context.setMemberProperties({'industry': value})
    industry = property(get_industry, set_industry)

    def get_primary_competencies(self):
        return self.context.getProperty('primary_competencies', '')
    def set_primary_competencies(self, value):
        return self.context.setMemberProperties({'primary_competencies': value})
    primary_competencies = property(get_primary_competencies, set_primary_competencies)

    def get_primary_competencies(self):
        return self.context.getProperty('primary_competencies', '')
    def set_primary_competencies(self, value):
        return self.context.setMemberProperties({'primary_competencies': value})
    primary_competencies = property(get_primary_competencies, set_primary_competencies)

    def get_secondary_competencies(self):
        return self.context.getProperty('secondary_competencies', '')
    def set_secondary_competencies(self, value):
        return self.context.setMemberProperties({'secondary_competencies': value})
    secondary_competencies = property(get_secondary_competencies, set_secondary_competencies)

    def get_user_biography(self):
        return self.context.getProperty('user_biography', '')
    def set_user_biography(self, value):
        return self.context.setMemberProperties({'user_biography': value})
    user_biography = property(get_user_biography, set_user_biography)

  