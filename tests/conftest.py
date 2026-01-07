import pytest

from genie_flow_invoker import GenieInvoker, InvokerFactory


@pytest.fixture
def invoker_factory():
    return InvokerFactory(None)
