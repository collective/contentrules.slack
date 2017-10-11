# -*- coding: utf-8 -*-
"""Init and utils."""
from prettyconf import config
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('contentrules.slack')

SLACK_WEBHOOK_URL = config('SLACK_WEBHOOK_URL', default='')
