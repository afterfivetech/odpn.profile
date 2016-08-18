from zope import schema
from five import grok
from plone.app.registry.browser.controlpanel import RegistryEditForm, ControlPanelFormWrapper
from Products.Five.browser import BrowserView
from plone.z3cform import layout
from plone.directives import form
from odpn.profile.interfaces import ICompetencies, ICompetencyDGForm
from z3c.form import form, field, button



    

class CompetencyForm(RegistryEditForm):
    schema = ICompetencyDGForm
    label = u"Competency Settings"
    
    def updateFields(self):
        super(CompetencyForm, self).updateFields()
    
    def updateWidgets(self):
        super(CompetencyForm, self).updateWidgets()
    
    
class CompetencyFormView(ControlPanelFormWrapper):
    form = CompetencyForm