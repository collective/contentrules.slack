from contentrules.slack import slack_notifier
from contextlib import contextmanager


class ResponseStub:
    def raise_for_status(self):
        pass


class RequestsMock:
    def __init__(self):
        self.posts = []

    def post(self, url, **kwargs):
        kwargs["url"] = url
        self.posts.append(kwargs)
        return ResponseStub()

    @classmethod
    @contextmanager
    def installed(kls):
        original_requests = slack_notifier.requests
        mock_requests = slack_notifier.requests = kls()
        try:
            yield mock_requests
        finally:
            slack_notifier.requests = original_requests
