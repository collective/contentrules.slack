"""Test layers for this package."""

from OFS.Application import Application
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import contentrules.slack


class SlackLayer(PloneSandboxLayer):
    """A Plone site with the default content types and this package's ZCML.

    The package has no GenericSetup profile: registering the ZCML is all it
    takes for the action to be offered in the content rules control panel.
    """

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app: Application, configurationContext) -> None:
        """Load this package's ZCML.

        :param app: The Zope application root.
        :param configurationContext: ZCML configuration context.
        """
        self.loadZCML(package=contentrules.slack)


FIXTURE = SlackLayer()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="SlackLayer:IntegrationTesting",
)
