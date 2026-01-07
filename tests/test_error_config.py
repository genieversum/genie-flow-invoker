import builtins

import yaml

from genie_flow_invoker import GenieInvoker, InvokerFactory


class TestInvoker(GenieInvoker):

    def invoke(self, content: str) -> str:
        return content

    @classmethod
    def from_config(cls, config: dict):
        return cls()


def test_none(invoker_factory):
    meta = """
type: tests.test_error_config.TestInvoker
    """
    config = yaml.safe_load(meta)
    invoker = invoker_factory.create_invoker(config)
    assert invoker._on_error_specs is None
    assert invoker._retry_specs is None


def test_on_error_template(invoker_factory):
    meta = """
type: tests.test_error_config.TestInvoker
on_error: This is a template with {{ some mustaches }}
    """
    config = yaml.safe_load(meta)
    invoker = invoker_factory.create_invoker(config)
    assert invoker._on_error_specs is not None
    assert invoker._retry_specs is None
    assert invoker._on_error_specs.event is None
    assert invoker._on_error_specs.content == "This is a template with {{ some mustaches }}"


def test_on_error_event(invoker_factory):
    meta = """
type: tests.test_error_config.TestInvoker
on_error:
    event: this_failed
    """
    config = yaml.safe_load(meta)
    invoker = invoker_factory.create_invoker(config)
    assert invoker._on_error_specs is not None
    assert invoker._retry_specs is None
    assert invoker._on_error_specs.event == "this_failed"
    assert invoker._on_error_specs.content is None


def test_on_error_event_content(invoker_factory):
    meta = """
type: tests.test_error_config.TestInvoker
on_error:
    event: this_failed
    content: FailingInvokerError
    """
    config = yaml.safe_load(meta)
    invoker = invoker_factory.create_invoker(config)
    assert invoker._on_error_specs is not None
    assert invoker._retry_specs is None
    assert invoker._on_error_specs.event == "this_failed"
    assert invoker._on_error_specs.content == "FailingInvokerError"


def test_retry_exception(invoker_factory):
    meta = """
type: tests.test_error_config.TestInvoker
retry:
    autoretry_for:
        - builtins.Exception
    """
    config = yaml.safe_load(meta)
    invoker = invoker_factory.create_invoker(config)
    assert invoker._on_error_specs is None
    assert invoker._retry_specs is not None
    assert builtins.Exception in invoker._retry_specs.autoretry_for


def test_retry_full(invoker_factory):
    meta = """
type: tests.test_error_config.TestInvoker
retry:
    autoretry_for:
        - builtins.Exception
    max_retries: 10
    retry_backoff: 2
    retry_backoff_max: 600
    retry_jitter: true
    """
    config = yaml.safe_load(meta)
    invoker = invoker_factory.create_invoker(config)
    assert invoker._on_error_specs is None
    assert invoker._retry_specs is not None
    assert builtins.Exception in invoker._retry_specs.autoretry_for
    assert invoker._retry_specs.max_retries == 10
    assert invoker._retry_specs.retry_backoff == 2
    assert invoker._retry_specs.retry_backoff_max == 600
    assert invoker._retry_specs.retry_jitter == True


def test_both(invoker_factory):
    meta = """
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
    config = yaml.safe_load(meta)
    invoker = invoker_factory.create_invoker(config)
    assert invoker._on_error_specs.event == "this_failed"
    assert invoker._on_error_specs.content == "FailingInvokerError"
    assert builtins.Exception in invoker._retry_specs.autoretry_for
    assert invoker._retry_specs.max_retries == 10
    assert invoker._retry_specs.retry_backoff == 2
    assert invoker._retry_specs.retry_backoff_max == 600
    assert invoker._retry_specs.retry_jitter == True
