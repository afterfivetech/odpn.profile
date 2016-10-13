try:
    from plone.stringinterp.adapters import BaseSubstitution
except ImportError:
    class BaseSubstitution(object):
        """ Fallback class if plone.stringinterp is not available
        """

        def __init__(self, context, **kwargs):
            self.context = context
            

class emailAddress(BaseSubstitution):
     category = u'Current User'
     description = u'Registration Email Address'
     
     def safe_call(self):
        context = self.context
        
        if hasattr(context, 'email_address'):
            return getattr(context, 'email_address', u'')
        return u''