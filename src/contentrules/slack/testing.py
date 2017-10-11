# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import contentrules.slack


class ContentrulesSlackLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=contentrules.slack)


CONTENTRULES_SLACK_FIXTURE = ContentrulesSlackLayer()


CONTENTRULES_SLACK_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CONTENTRULES_SLACK_FIXTURE,),
    name='ContentrulesSlackLayer:IntegrationTesting'
)


CONTENTRULES_SLACK_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CONTENTRULES_SLACK_FIXTURE,),
    name='ContentrulesSlackLayer:FunctionalTesting'
)


CONTENTRULES_SLACK_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CONTENTRULES_SLACK_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='ContentrulesSlackLayer:AcceptanceTesting'
)
