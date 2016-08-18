from zope.interface import Interface
from zope import schema
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.directives import dexterity, form

class IProductSpecific(Interface):
    pass


class ICompetencies(Interface):
    primary_competencies_values = schema.TextLine(
        title=u"Competency Values"
    )

class ICompetencyDGForm(Interface):
    
    form.widget(competencies=DataGridFieldFactory)
    competencies = schema.List(
        title=u"Competency Values",
        required=False,
        value_type=DictRow(title=u"Value", schema=ICompetencies)
    )
