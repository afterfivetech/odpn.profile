from collective.grok import gs
from odpn.profile import MessageFactory as _

@gs.importstep(
    name=u'odpn.profile', 
    title=_('odpn.profile import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('odpn.profile.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
