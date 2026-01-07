import builtins

from genie_flow_invoker import GenieInvoker


class TestInvoker(GenieInvoker):

    def invoke(self, content: str) -> str:
        return content

    @classmethod
    def from_config(cls, config: dict):
        return cls()


def test_none(invoker_factory):
    """
type: tests.test_error_config.TestInvoker
    """
    config = {
        "type": "tests.test_error_config.TestInvoker"
    }
    invoker = invoker_factory.create_invoker(config)
    assert invoker._on_error_specs is None
    assert invoker._retry_specs is None


def test_on_error_template(invoker_factory):
    """
type: tests.test_error_config.TestInvoker
on_error: This is a template with {{ some mustaches }}
    """
    config = {
        "type": "tests.test_error_config.TestInvoker",
        "on_error": "This is a template with {{ some mustaches }}",
    }
    invoker = invoker_factory.create_invoker(config)
    assert invoker._on_error_specs is not None
    assert invoker._retry_specs is None
    assert invoker._on_error_specs.event is None
    assert invoker._on_error_specs.content == "This is a template with {{ some mustaches }}"


def test_on_error_event(invoker_factory):
    """
type: tests.test_error_config.TestInvoker
on_error:
    event: this_failed
    """
    config = {
        "type": "tests.test_error_config.TestInvoker",
        "on_error": {
            "event": "this_failed",
        },
    }
    invoker = invoker_factory.create_invoker(config)
    assert invoker._on_error_specs is not None
    assert invoker._retry_specs is None
    assert invoker._on_error_specs.event == "this_failed"
    assert invoker._on_error_specs.content is None


def test_on_error_event_content(invoker_factory):
    """
type: tests.test_error_config.TestInvoker
on_error:
    event: this_failed
    content: FailingInvokerError
    """
    config = {
        "type": "tests.test_error_config.TestInvoker",
        "on_error": {
            "event": "this_failed",
            "content": "FailingInvokerError",
        },
    }
    invoker = invoker_factory.create_invoker(config)
    assert invoker._on_error_specs is not None
    assert invoker._retry_specs is None
    assert invoker._on_error_specs.event == "this_failed"
    assert invoker._on_error_specs.content == "FailingInvokerError"


def test_retry_exception(invoker_factory):
    """
type: tests.test_error_config.TestInvoker
retry:
    autoretry_for:
        - builtins.Exception
    """
    config = {
        "type": "tests.test_error_config.TestInvoker",
        "retry": {
            "autoretry_for": ["builtins.Exception"],
        },
    }
    invoker = invoker_factory.create_invoker(config)
    assert invoker._on_error_specs is None
    assert invoker._retry_specs is not None
    assert builtins.Exception in invoker._retry_specs.autoretry_for


def test_retry_full(invoker_factory):
    """
type: tests.test_error_config.TestInvoker
retry:
    autoretry_for:
        - builtins.Exception
    max_retries: 10
    retry_backoff: 2
    retry_backoff_max: 600
    retry_jitter: true
    """
    config = {
        "type": "tests.test_error_config.TestInvoker",
        "retry": {
            "autoretry_for": ["builtins.Exception"],
            "max_retries": 10,
            "retry_backoff": 2,
            "retry_backoff_max": 600,
            "retry_jitter": True,
        },
    }
    invoker = invoker_factory.create_invoker(config)
    assert invoker._on_error_specs is None
    assert invoker._retry_specs is not None
    assert builtins.Exception in invoker._retry_specs.autoretry_for
    assert invoker._retry_specs.max_retries == 10
    assert invoker._retry_specs.retry_backoff == 2
    assert invoker._retry_specs.retry_backoff_max == 600
    assert invoker._retry_specs.retry_jitter == True


def test_both(invoker_factory):
    """
type: tests.test_error_config.TestInvoker
on_error:
    event: this_failed
    content: FailingInvokerError
retry:
    autoretry_for:
        - builtins.Exception
    max_retries: 10
    retry_backoff: 2
    retry_backoff_max: 600
    retry_jitter: true
    """
    config = {
        "type": "tests.test_error_config.TestInvoker",
        "on_error": {
            "event": "this_failed",
            "content": "FailingInvokerError",
        },
        "retry": {
            "autoretry_for": ["builtins.Exception"],
            "max_retries": 10,
            "retry_backoff": 2,
            "retry_backoff_max": 600,
            "retry_jitter": True,
        },
    }
    invoker = invoker_factory.create_invoker(config)
    assert invoker._on_error_specs.event == "this_failed"
    assert invoker._on_error_specs.content == "FailingInvokerError"
    assert builtins.Exception in invoker._retry_specs.autoretry_for
    assert invoker._retry_specs.max_retries == 10
    assert invoker._retry_specs.retry_backoff == 2
    assert invoker._retry_specs.retry_backoff_max == 600
    assert invoker._retry_specs.retry_jitter == True
