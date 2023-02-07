from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import contentrules.slack


class CRSlackLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=contentrules.slack)


CRSLACK_FIXTURE = CRSlackLayer()


CRSLACK_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CRSLACK_FIXTURE,),
    name="CRSlackLayer:IntegrationTesting",
)
