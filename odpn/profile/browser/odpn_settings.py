from five import grok
from Products.CMFCore.interfaces import ISiteRoot
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from odpn.profile.interfaces import ICompetencyDGForm

grok.templatedir('templates')

class odpn_settings(grok.View):
    grok.name('odpn-settings')
    grok.context(ISiteRoot)
    
    def list_competencies(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICompetencyDGForm, check=False)
        if settings.competencies:
            return [val['primary_competencies_values'] for val in settings.competencies]
        return []